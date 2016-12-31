import uuid
from datetime import datetime


from cassandra.cqlengine.columns import UUID, Text, DateTime, Float
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

from currencies import CURRENCIES


class CurrencyPair(Model):
    id = UUID(primary_key=True, default=uuid.uuid4)
    base = Text(required=True)
    counter = Text(required=True)

    def validate(self):
        super(CurrencyPair, self).validate()
        if self.base not in CURRENCIES or self.counter not in CURRENCIES:
            raise ValidationError('Invalid Currency Pair: {}/{}'.format(self.base, self.counter))


class CurrencyPairValue(Model):
	id = UUID(primary_key=True, default=uuid.uuid4)
	base = Text(required=True)
	counter = Text(required=True)
	date = DateTime(primary_key=True, clustering_order="DESC")
	open = Float()
	close = Float()
	high = Float()
	low = Float()
	volume = Float()

	def validate(self):
		super(CurrencyPairValue, self).validate()
		if self.base not in CURRENCIES or self.counter not in CURRENCIES:
		    raise ValidationError('Invalid Currency Pair: {}/{}'.format(self.base, self.counter))

