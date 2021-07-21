import pandas as pd
import llog


# https://stackoverflow.com/questions/47466255/subclassing-a-pandas-dataframe-updates
class LLogSeries(pd.Series):
    _metadata = ['meta']

    @property
    def _constructor(self):
        return LLogSeries

    @property
    def _constructor_expanddim(self):
        return LLogDataFrame

    def plot(self, *args, **kwargs):
        print('plotnig', self.meta)
        meta = self.meta

        kwargs = kwargs | meta
        ax = super().plot(*args, **kwargs)
        ax.legend()

        name = meta['name']
        units = f' {meta["units"]}'
        # color = f'{meta["color"]}'
        # marker = f'{meta["marker"]}'

        ax.set_ylabel(f'{name}{units}')
        return ax


    
# https://stackoverflow.com/questions/48325859/subclass-pandas-dataframe-with-required-argument
class LLogDataFrame(pd.DataFrame):
    _metadata = ['meta']

    @property
    def _constructor(self):
        return LLogDataFrame

    @property
    def _constructor_sliced(self):
        def _c(*args, **kwargs):
            s = LLogSeries(*args, **kwargs)
            try:
                name = kwargs['name']
                meta = self.meta[name]
                s.meta = meta
            except:
                pass
            return s
        return _c

    def plot(self, *args, **kwargs):
        for c in self:
            self[c].plot(*args, **kwargs)
# a = LLogSeries(['a','a'], name='A')
# b = LLogSeries(['b','b'], name='B')
# c = LLogSeries(['c','c'], name='C')

# 
# a.metas = 'ameta'
# b.metas = 'bmeta'
# c.metas = 'cmeta'
dfmeta = {
    "one": "metaone",
    "two": "metatwo",
    "three": "metathree",
}
# df = LLogDataFrame({"one": a, "two":b, "three":c}, index=None)
df = LLogDataFrame({"one": ['a','a'], "two":['b','b'], "three":['c','c']}, index=None)

df.meta = dfmeta

print(f'ameta {df["one"].meta}')
df2 = df[['one','two']]
print(f'df2meta: {df2.meta}')
print(f'df2meta: {df2["one"].meta}')

# df2['one'].plot()
df2.plot()