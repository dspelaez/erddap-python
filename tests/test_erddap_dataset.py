import pytest 
from pyerddap import ERDDAP_Tabledap

@pytest.mark.vcr()
def test_remote_connection():
    url = 'https://coastwatch.pfeg.noaa.gov/erddap'
    datasetid = 'cwwcNDBCMet'
    remote = ERDDAP_Tabledap(url, datasetid, 'tabledap')
    datasetTitle = remote.getAttribute('title')
    assert datasetTitle == 'NDBC Standard Meteorological Buoy Data, 1970-present'


def test_request_url():
    url = 'https://coastwatch.pfeg.noaa.gov/erddap'
    datasetid = 'cwwcNDBCMet'
    remote = ERDDAP_Tabledap(url, datasetid)
    (
    remote.setResultVariables(['station','time','atmp'])
          .addConstraint('time>=2020-12-24T00:00:00Z')
          .addConstraint('time<=2020-12-31T01:15:00Z')
          .orderBy(['station'])
    )
    orderbyurl_test = remote.getDataRequestURL()
    remote.clearQuery()

    (
    remote.setResultVariables(['station','time','atmp'])
          .addConstraint('time>=2020-12-24T00:00:00Z')
          .addConstraint('time<=2020-12-31T01:15:00Z')
          .orderByClosest(['station','time/1day'])
    )
    orderbyclosest_test = remote.getDataRequestURL()
    remote.clearQuery()

    print (orderbyurl_test)
    assert orderbyurl_test == 'https://coastwatch.pfeg.noaa.gov/erddap/tabledap/cwwcNDBCMet.csvp?station%2Ctime%2Catmp&time%3E=2020-12-24T00%3A00%3A00Z&time%3C=2020-12-31T01%3A15%3A00Z&orderBy(%22station%22)'
    
    print (orderbyclosest_test)
    assert orderbyclosest_test == 'https://coastwatch.pfeg.noaa.gov/erddap/tabledap/cwwcNDBCMet.csvp?station%2Ctime%2Catmp&time%3E=2020-12-24T00%3A00%3A00Z&time%3C=2020-12-31T01%3A15%3A00Z&orderByClosest(%22station%2Ctime/1day%22)'


def test_getattribute():
    url = 'https://coastwatch.pfeg.noaa.gov/erddap'
    datasetid = 'cwwcNDBCMet'
    remote = ERDDAP_Tabledap(url, datasetid)

    dsttitle = remote.getAttribute('title')
    dstwspd_comment = remote.getAttribute('comment','wspd')

    assert dsttitle == 'NDBC Standard Meteorological Buoy Data, 1970-present'
    assert dstwspd_comment == 'Average wind speed (m/s).'