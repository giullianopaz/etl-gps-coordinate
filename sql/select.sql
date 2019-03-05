SELECT  Point.pointLAT,
        Point.pointLNG,
        Point.pointStreetName,
        Point.pointHouseNumber, 
        Suburb.suburbName,
        City.cityName,
        Point.pointPostalCode,
        State.stateUF,
        Country.countryName 
FROM Point
LEFT JOIN Suburb
ON Point.suburbID = Suburb.id
LEFT JOIN City
ON Suburb.cityID = City.id
LEFT JOIN State
ON City.stateID = State.id
LEFT JOIN Country
ON State.countryID = Country.id;