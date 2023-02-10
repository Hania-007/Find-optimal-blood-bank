# Find-optimal-blood-bank
## About
Given hospital address and blood type find from which blood bank (in Poland) it is the most optimal to take the missing blood.

Data taken from the site: https://krew.info/zapasy/

Used APIs:
- https://pl-blood-supply-api.vercel.app/openapi/swagger#/Blood%20supply/getBloodSupplyEndpoint_blood_supply_get
- https://nominatim.org/release-docs/latest/api/Search/

## Launch

To launch the script pass 2 arguments: "your adress" "blood type".

Example:

<sup> python3 main.py "Karmelicka 2, Kraków, Polska" "A Rh+" </sup>

