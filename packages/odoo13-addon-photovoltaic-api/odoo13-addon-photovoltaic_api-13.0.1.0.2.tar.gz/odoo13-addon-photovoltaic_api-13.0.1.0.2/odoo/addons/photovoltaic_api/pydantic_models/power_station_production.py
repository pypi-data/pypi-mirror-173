from datetime import date

from .orm_model import OrmModel


class PowerStationProduction(OrmModel):
    date: date
    energy_generated: float