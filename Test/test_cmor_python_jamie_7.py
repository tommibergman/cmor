import cmor
import numpy
import unittest


class TestCase(unittest.TestCase):

    def testJamie7(self):
        try:
            cmor.setup(inpath='Test', netcdf_file_action=cmor.CMOR_REPLACE)

            cmor.dataset_json("Test/common_user_input.json")


            # creates 1 degree grid
            nlat = 18
            nlon = 36
            alats = numpy.arange(180) - 89.5
            bnds_lat = numpy.arange(181) - 90
            alons = numpy.arange(360) + .5
            bnds_lon = numpy.arange(361)
            cmor.load_table("Tables/CMIP6_Amon.json")
            ilat = cmor.axis(
                table_entry='latitude',
                units='degrees_north',
                length=nlat,
                coord_vals=alats,
                cell_bounds=bnds_lat)

            ilon = cmor.axis(
                table_entry='longitude',
                length=nlon,
                units='degrees_east',
                coord_vals=alons,
                cell_bounds=bnds_lon)

            ntimes = 12
            plevs = numpy.array([100000., 92500, 85000, 70000, 60000, 50000, 40000, 30000, 25000,
                                20000, 15000, 10000, 7000, 5000, 3000, 2000, 1000, 999, 998, 997, 996,
                                995, 994, 500, 100])


            itim = cmor.axis(
                table_entry='time',
                units='months since 2030-1-1',
                length=ntimes,
                interval='1 month')

            ilev = cmor.axis(
                table_entry='plev19',
                units='Pa',
                coord_vals=plevs,
                cell_bounds=None)


            var3d_ids = cmor.variable(
                table_entry='ta',
                units='K',
                axis_ids=numpy.array((ilev, ilon, ilat, itim)),
                missing_value=numpy.array([1.0e28, ], dtype=numpy.float32)[0],
                original_name='cloud')


            for it in range(ntimes):

                time = numpy.array((it))
                bnds_time = numpy.array((it, it + 1))
                data3d = numpy.random.random((len(plevs), nlon, nlat)) * 30. + 265.
                data3d = data3d.astype('f')
                cmor.write(
                    var_id=var3d_ids,
                    data=data3d,
                    ntimes_passed=1,
                    time_vals=time,
                    time_bnds=bnds_time)

            cmor.close()
        except BaseException:
            raise
            

if __name__ == '__main__':
    unittest.main()
