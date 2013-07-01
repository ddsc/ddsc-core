import logging

logger = logging.getLogger(__name__)

# EPSG:28992
RD = ("+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 "
      "+k=0.999908 +x_0=155000 +y_0=463000 +ellps=bessel "
      "+towgs84=565.237,50.0087,465.658,-0.406857,0.350733,-1.87035,4.0812 "
      "+units=m +no_defs")


def transform(the_geom, srid, clone=False):
    """Perform a geometry transformation.

    the_geom: a GEOSGeometry
    srid: an integer SRID
    clone: if False, perform an in-place geometry transformation (the default)

    GEOS transform() is not accurate for 28992.
    The infamous towgs84 parameter is missing?

    This particular problem can be solved by adding the ubuntugis-stable PPA to
    your system. Apparently, the Ubuntu version we are using - 12.04 - has old
    geospatial libraries in its repositories. Upgrading, however, caused other
    problems (viz. a segfault in combination with pyproj), so we revert to
    this workaround.

    """

    if srid == 28992:
        the_geom2 = the_geom.transform(RD, clone)
    else:
        the_geom2 = the_geom.transform(srid, clone)

    if not clone:
        return the_geom
    else:
        return the_geom2
