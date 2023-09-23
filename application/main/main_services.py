from sqlalchemy import text
from application import db


def get_main_verifications(fromdate, todate):
    datasql = text(
    """
        Select
            Case
                When Trim(lc.county_name) = 'Tharaka-Nithi'
                Then 'Tharaka'
                When Trim(lc.county_name) = 'Nairobi City'
                Then 'Nairobi'
                When Trim(lc.county_name) = 'Muranga'
                Then 'Murang''a'
                        When Trim(lc.county_name) = 'Elgeyo Marakwet'
                Then 'Keiyo-Marakwet'
                Else Trim(lc.county_name)
            End As county_name,
            COALESCE(v.visits, 0) as visits
        From
            system_location_counties lc Left Join
            (Select
                c.county_name,
                c.system_location_counties_serial,
                Count(vv.nhif_hospital_visit_serial) As visits
            From
                nhif_hospital_visits vv Inner Join
                nhif_hospitals h On vv.nhif_hospital_serial = h.nhif_hospital_serial Inner Join
                system_branches b On h.system_branch_serial = b.system_branch_serial Inner Join
                system_location_sub_counties sc On b.system_location_sub_county_serial = sc.system_location_sub_county_serial
                Inner Join
                system_location_counties c On sc.system_location_counties_serial = c.system_location_counties_serial
            Where
                vv.date_added::date >= CURRENT_DATE -7  AND
                vv.date_added::date <=CURRENT_DATE
            Group By
                c.county_name,
                c.system_location_counties_serial) v On v.system_location_counties_serial = lc.system_location_counties_serial
        """
    )
    params = {"fromdate": fromdate, "todate": todate}
    sqldata = db.get_engine(bind="netoffice").execute(datasql, params).fetchall()
    return sqldata
