# SiPM_model
a monte-carlo simulation of SiPM pulse types and various associated noise contributions

# Truth Data Table

## Afterpulse truth data:
0 : Number of afterpulses
## followed by pairs of:
1 : Amplitude of afterpulse
2 : Position of afterpulses

## Crosstalk truth data
0 : Number of prompt cross talk pulses
1 : Number of Delayed cross talk pulses
followed by:
2 : Positions of delayed cross talk pulses

# Parameter data table

0: Scale
1: onset time
2: rise time constant
3: short decay time constant
4: long decay time constant
5: a (left root of quadratic)
6: b (right root of quadratic)

# data found format

0: counted afterpulses
1: counted prompt crosstalks
2: counted delayed crosstalks
3: truth afterpulses
4: truth prompt crosstalks
5: truth delayed crosstalks

