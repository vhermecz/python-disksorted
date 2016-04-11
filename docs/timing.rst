==============  ========  ============  =============  ==============  ============
conf            sorted    disksorted    disksorted     disksorted      disksorted
                          chunksize=1K  chunksize=10K  chunksize=100K  chunksize=1M
simple,10k      1.92ms    176%          na             na              na
simple,1m       561.78ms  77%           78%            119%            na
simple,10m      8.99s     toomany       toomany        101%            116%
simple,100m     2.52m     toomany       toomany        83%             98%
pload:0,10k     5.91ms    555%          na             na              na
pload:0,1m      1.81s     192%          201%           224%            na
pload:32,10k    5ms       652%          na             na              na
pload:0,1m      1.71s     203%          209%           236%            na
pload:0-2k,10k  4.99ms    956%          na             na              na
pload:0-2k,1m   1.88s     404%          481%           504%            na
==============  ========  ============  =============  ==============  ============