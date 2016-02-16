# Global imports (used ubiquitously throughout this module.
from spacepy.datamodel import dmarray, SpaceData
import numpy as np
from spacepy.pybats import PbData


class IdlBin(PbData):
    '''
    An object class that reads/parses a binary output file from the SWMF
    and places it into a :class:spacepy.pybats.PbData object.

    Usage:
    >>>data = spacepy.pybats.IdlBin('binary_file.out')

    See :class:`spacepy.pybats.PbData` for information on how to explore
    data contained within the returned object.

    This class serves as a parent class to SWMF component-specific derivative
    classes that do more preprocessing of the data before returning the 
    object.  Hence, using this class to read binary files is typically not
    the most efficient way to proceed.  Look for a PyBats sub module that suits
    your specific needs, or use this base object to write your own.

    A note on byte-swapping: PyBats assumes little endian byte ordering because
    this is what most machines use.  However, there is an autodetect feature
    such that, if PyBats doesn't make sense of the first read (a record length
    entry, or RecLen), it will proceed using big endian ordering.  If this
    doesn't work, the error will manifest itself through the "struct" package
    as an "unpack requires a string of argument length 'X'".
    '''

    def __init__(self, filename, *args, **kwargs):
        super(IdlBin, self).__init__(*args, **kwargs)  # Init as PbData.
        self.attrs['file'] = filename  # Save file name.
        self.read()  # Read binary file.

    def __repr__(self):
        return 'SWMF IDL-Binary file "%s"' % (self.attrs['file'])

    def read(self):
        '''
        This method reads an IDL-formatted BATS-R-US output file and places
        the data into the object.  The file read is self.filename which is
        set when the object is instantiation.
        '''
        import numpy as np
        import struct

        # Open, read, and parse the file into numpy arrays.
        # Note that Fortran writes integer buffers around records, so
        # we must parse those as well.
        infile = open(self.attrs['file'], 'rb')

        # On the first try, we may fail because of wrong-endianess.
        # If that is the case, swap that endian and try again.
        EndChar = '<'  # Endian marker (default: little.)
        self.attrs['endian'] = 'little'
        RecLenRaw = infile.read(4)

        RecLen = (struct.unpack(EndChar + 'l', RecLenRaw))[0]
        if (RecLen > 10000) or (RecLen < 0):
            EndChar = '>'
            self.attrs['endian'] = 'big'
            RecLen = (struct.unpack(EndChar + 'l', RecLenRaw))[0]

        header = (struct.unpack(EndChar + '%is' % RecLen,
                                infile.read(RecLen)))[0]
        header.strip()
        units = header.split()

        (OldLen, RecLen) = struct.unpack(EndChar + '2l', infile.read(8))
        format = 'f'
        # parse header; detect double-precision file.
        if RecLen > 20: format = 'd'
        (self.attrs['iter'], self.attrs['time'],
         self.attrs['ndim'], self.attrs['nparam'], self.attrs['nvar']) = \
            struct.unpack(EndChar + 'l%s3l' % format, infile.read(RecLen))
        # Get gridsize
        (OldLen, RecLen) = struct.unpack(EndChar + '2l', infile.read(8))
        self['grid'] = dmarray(struct.unpack(EndChar + '%il' %
                                             abs(self.attrs['ndim']),
                                             infile.read(RecLen)))
        # Data from generalized (structured but irregular) grids can be 
        # detected by a negative ndim value.  Unstructured grids (e.g.
        # BATS, AMRVAC) are signified by negative ndim values AND
        # the grid size is always [x, 1(, 1)]
        # Here, we set the grid type attribute to either Regular, 
        # Generalized, or Unstructured.  Let's set that here.
        self['grid'].attrs['gtype'] = 'Regular'
        self['grid'].attrs['npoints'] = abs(self['grid'].prod())
        if self.attrs['ndim'] < 0:
            if any(self['grid'][1:] > 1):
                self['grid'].attrs['gtype'] = 'Generalized'
            else:
                self['grid'].attrs['gtype'] = 'Unstructured'
                self['grid'].attrs['npoints'] = self['grid'][0]
        self.attrs['ndim'] = abs(self.attrs['ndim'])

        # Quick ref vars:
        time = self.attrs['time']
        gtyp = self['grid'].attrs['gtype']
        npts = self['grid'].attrs['npoints']
        ndim = self['grid'].size
        nvar = self.attrs['nvar']
        npar = self.attrs['nparam']

        # Read parameters stored in file.
        (OldLen, RecLen) = struct.unpack(EndChar + '2l', infile.read(8))
        para = np.zeros(npar)
        para[:] = struct.unpack(EndChar + '%i%s' % (npar, format),
                                infile.read(RecLen))

        (OldLen, RecLen) = struct.unpack(EndChar + '2l', infile.read(8))

        print EndChar + '%is' % RecLen
        names = (struct.unpack(EndChar + '%is' % RecLen,
                               infile.read(RecLen)))[0].lower()
        names.strip()
        names = names.split()

        # For some reason, there are often more units than variables
        # in these files.  It looks as if there are more grid units
        # than grid vectors (e.g. 'R R R' implies X, Y, and Z data
        # in file but only X and Y are present.)  Let's try to work
        # around this rather egregious error.
        nSkip = len(units) + npar - len(names)
        if nSkip < 0: nSkip = 0
        # Some debug crap:
        # print "nSkip=", nSkip
        # for n, u in zip(names, units[nSkip:]):
        #     print n, u

        # Save grid names (e.g. 'x' or 'r') and save associated params.
        self['grid'].attrs['dims'] = names[0:ndim]
        for name, para in zip(names[(nvar + ndim):], para):
            self.attrs[name] = para

        # Create string representation of time.
        self.attrs['strtime'] = '%4.4ih%2.2im%06.3fs' % \
                                (np.floor(time / 3600.), np.floor(time % 3600. / 60.0),
                                 time % 60.0)

        # Get the grid points...
        (OldLen, RecLen) = struct.unpack(EndChar + '2l', infile.read(8))

        prod = [1] + self['grid'].cumprod().tolist()

        for i in range(0, ndim):
            tempgrid = np.array(struct.unpack(
                EndChar + '%i%s' % (npts, format),
                infile.read(RecLen / ndim)))
            # Unstructred grids get loaded as vectors.
            if gtyp == 'Unstructured':
                self[names[i]] = dmarray(tempgrid)
            # Irregularly gridded items need multidimensional grid arrays:
            elif gtyp == 'Irregular':
                self[names[i]] = dmarray(
                    np.reshape(tempgrid, self['grid']))
            # Regularly gridded ones need vector grid arrays:
            elif gtyp == 'Regular':
                self[names[i]] = dmarray(np.zeros(self['grid'][i]))
                for j in range(int(self['grid'][i])):
                    self[names[i]][j] = tempgrid[j * int(prod[i])]
            else:
                raise ValueError('Unknown grid type: %s' % self.gridtype)
            # Add units to grid.
            self[names[i]].attrs['units'] = units.pop(nSkip)

        # Get the actual data and sort.
        for i in range(ndim, nvar + ndim):
            (OldLen, RecLen) = struct.unpack(EndChar + '2l', infile.read(8))
            # print EndChar + '%i%s' % (npts, format), RecLen
            self[names[i]] = dmarray( \
                np.array(struct.unpack(EndChar + '%i%s' % (npts, format),
                                       infile.read(RecLen))))

            print self[names[i]][14234]
            self[names[i]].attrs['units'] = units.pop(nSkip)
            if gtyp != 'Unstructured':
                # Put data into multidimensional arrays.
                self[names[i]] = self[names[i]].reshape(self['grid'])

        # Unstructured data can be in any order, so let's sort it.
        if gtyp == 'Unstructured':
            gridtotal = np.zeros(npts)
            offset = 0.0  # The offset ensures no repeating vals while sorting.
            for key in self['grid'].attrs['dims']:
                gridtotal = gridtotal + offset + self[key]
                offset = offset + np.pi / 2.0
                SortIndex = np.argsort(gridtotal)
            for key in list(self.keys()):
                if key == 'grid': continue
                self[key] = self[key][SortIndex]

        infile.close()


file = IdlBin("/Users/artem/workspace/inasan/SWMF/src/run/GM/IO2/z=0_ful_1_t00000000_n00000000.out")
