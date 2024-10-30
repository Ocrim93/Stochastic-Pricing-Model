#ifndef BLACKSCHOLES_H
#define BLACKSCHOLES_H
#include "../Payoff/Payoff.h"

double BlackScholesPathIndependent(const PayOff& thePayOff,
									double Spot,
									double Vol,
									double r,
									double q,
									unsigned long NumberOfPaths);

#endif

