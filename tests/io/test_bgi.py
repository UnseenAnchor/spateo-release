from unittest import TestCase

import spateo.io.bgi as bgi
from ..mixins import TestMixin


class TestIOBGI(TestMixin, TestCase):
    def test_read_bgi_as_dataframe(self):
        df = bgi.read_bgi_as_dataframe(self.bgi_counts_path)
        self.assertEqual(
            {"geneID": "0610009B22Rik", "x": 9776, "y": 12669, "MIDCounts": 1},
            df.iloc[0].to_dict(),
        )
        self.assertEqual(77634, df.shape[0])

    def test_read_bgi_agg(self):
        adata = bgi.read_bgi_agg(self.bgi_counts_path, scale=1, scale_unit="a")
        self.assertNotIn("spliced", adata.layers)
        self.assertNotIn("unspliced", adata.layers)
        self.assertIn("spatial", adata.uns)
        self.assertEqual(1, adata.uns["spatial"]["scale"])
        self.assertEqual("a", adata.uns["spatial"]["scale_unit"])
        self.assertEqual(1, adata.uns["spatial"]["binsize"])
        self.assertEqual(9600, adata.uns["spatial"]["x_min"])
        self.assertEqual(12600, adata.uns["spatial"]["y_min"])
        self.assertIn("pp", adata.uns)
        self.assertEqual((299, 300), adata.shape)