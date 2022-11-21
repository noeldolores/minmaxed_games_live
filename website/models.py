from sqlalchemy.dialects.mysql import DECIMAL
from datetime import datetime
from . import db


class Market(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    server_id = db.Column(db.Integer)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.relationship('Item', backref=db.backref('market'))
    
    
class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  item_id = db.Column(db.String(150))
  name = db.Column(db.String(150))
  price = db.Column(DECIMAL(38,15))
  availability = db.Column(db.Integer)
  market_id = db.Column(db.Integer, db.ForeignKey(Market.id))
  
class ItemData(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ItemType = db.Column(db.String(150))
  ItemClass = db.Column(db.String(150))
  Tier = db.Column(db.Integer)
  ItemID = db.Column(db.String(150))
  Name	= db.Column(db.String(150)) # Import Data from: javelindata_itemdefinitions_master.loc.xml
  ItemTypeDisplayName	= db.Column(db.String(150)) # string replace
  Description	= db.Column(db.String(150)) # Import Data from: javelindata_itemdefinitions_master.loc.xml
  TradingCategory	= db.Column(db.String(150))
  TradingFamily	= db.Column(db.String(150))
  TradingGroup	= db.Column(db.String(150))
  BindOnPickup	= db.Column(db.Integer)
  BindOnEquip	= db.Column(db.Integer)
  GearScoreOverride	= db.Column(db.Integer)
  MinGearScore	= db.Column(db.Integer)
  MaxGearScore	= db.Column(db.Integer)
  ItemStatsRef	= db.Column(db.String(150))
  CanHavePerks	= db.Column(db.Integer)
  CanReplaceGem	= db.Column(db.Integer)
  Perk1	= db.Column(db.String(150)) # Import Data from: javelindata_perks.loc.xml (description/name) ; javelindata_affixstats.datasheet (numerical values) ; javelindata_ability_global.datasheet (global perk values)
  Perk2	= db.Column(db.String(150)) # Import Data from: javelindata_perks.loc.xml
  Perk3	= db.Column(db.String(150)) # Import Data from: javelindata_perks.loc.xml
  Perk4	= db.Column(db.String(150)) # Import Data from: javelindata_perks.loc.xml
  Perk5	= db.Column(db.String(150)) # Import Data from: javelindata_perks.loc.xml
  ForceRarity	= db.Column(db.Integer)
  RequiredLevel	= db.Column(db.Integer)
  UseTypeAffix	= db.Column(db.Integer)
  UseMaterialAffix = db.Column(db.Integer)
  UseMagicAffix	= db.Column(db.Integer)
  IconCaptureGroup	= db.Column(db.Integer)
  UiItemClass	= db.Column(db.String(150))
  ArmorAppearanceM	= db.Column(db.String(150)) # Reference Self.value path to picture
  ArmorAppearanceF	= db.Column(db.String(150)) # Reference Self.value path to picture
  WeaponAppearanceOverride	= db.Column(db.String(150)) # Reference Self.value path to picture
  IconPath	= db.Column(db.String(150))	# Change path to server file format
  CraftingRecipe	= db.Column(db.String(150)) # Import Data from: javelindata_crafting.datasheet
  IngredientCategories	= db.Column(db.String(150))
  Durability	= db.Column(db.Integer)
  Weight	= db.Column(db.Integer)
  AttributionId = db.Column(db.String(150))
  DerivedFrom = db.Column(db.String(150)) # source javelindata_tooltiplayout.loc
  RefinedAt = db.Column(db.String(150)) # source javelindata_tooltiplayout.loc
  CraftedAt = db.Column(db.String(150)) # source javelindata_tooltiplayout.loc
  Cooldown	= db.Column(db.String(150))
  EffectDuration	= db.Column(db.String(150))