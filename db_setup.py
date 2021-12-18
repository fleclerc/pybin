#%%
from db import db
#%%
db.longshort.create_index( [("timestamp", 1)] )
#%%
db.depth.create_index( [("E", 1)] )

#%%
db.trades.create_index( [("eventTime", 1)] )

# %%
