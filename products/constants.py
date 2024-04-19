"""
Constants to be used in product models
"""

CODE_POSITION_CHOICES = (
    ('FOP', 'Front of pack'),
    ('BOP', 'Back of pack'),
    ('SOP', 'Side of pack'),
    ('Lid', 'Lid'),
    ('Sticker', 'Sticker'),
    ('BackingCard', 'BackingCard'),
    ('Insert', 'Insert'),
    ('OuterFOP', 'Outer front of pack'),
    ('OuterBOP', 'Outer Back of Pack'),
    ('InsidePack', 'InsidePack'),
    ('POS', 'Point of Sale'),
    ('PrintAd', 'PrintAd')
)
QR_CODE_BLOB_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=qrdownloadtest;AccountKey=KsOMid6XarBdmRDWFPkWoXb1sOoNEj+JTNosCNJHZDOCeInKhJloIt807J+P/4lXCIPzYTLGvvQd+AStVddepQ==;EndpointSuffix=core.windows.net"
QR_CODE_BLOB_STORAGE_CONTAINER_NAME = "qrcodes"