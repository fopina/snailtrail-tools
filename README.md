# snailtrail coefficent tracker

Script to track [SnailTrail](https://www.snailtrail.art/) incubation coefficent values over time.

[SnailTrail](https://www.snailtrail.art/) does not expose the coefficent in the UI except when you are about to incubate, but to incubate you need to have breeders available.

Yet, the contract method `getCurrentCoefficent` is available to call without any restrictions.

This script is scheduled to call that method and log values (over time) [data branch](https://github.com/fopinappb/snailtest/blob/data/log.bin).

That binary log is decoded and turned into a chart for visualization [here](https://fopina.github.io/snailtrail-tools/). Use it to predict the best time to breed!
