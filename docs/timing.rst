==============  ========  ============  =============  ==============  ============
conf            sorted    disksorted    disksorted     disksorted      disksorted
                          chunksize=1K  chunksize=10K  chunksize=100K  chunksize=1M
simple,10k      1.99ms    157%          na             na              na
simple,1m       543.04ms  72%           78%            123%            na
pload:0,10k     4.61ms    661%          na             na              na
pload:0,1m      1.69s     190%          196%           218%            na
pload:32,10k    5.64ms    591%          na             na              na
pload:0,1m      1.74s     199%          203%           227%            na
pload:0-2k,10k  5.15ms    937%          na             na              na
pload:0-2k,1m   1.65s     312%          302%           403%            na
==============  ========  ============  =============  ==============  ============