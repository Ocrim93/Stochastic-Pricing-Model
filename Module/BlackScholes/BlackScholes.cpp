#include "BlackScholes.h"
#include "../Random/Random.h"
#include <cmath>


double BlackScholesPathIndependent( double Expiry,
									double Strike,
									double Spot,
									double Vol,
									double r,
									double q,
									unsigned long NumberOfPaths){

	double fixedPart = (r - Vol*Vol/2)*Expiry;
	double sumPayOff = 0 ;

	for (unsigned long i = 0 ; i < NumberOfPaths; i++){
		double final_S = Spot*exp(fixedPart +  Vol*sqrt(Expiry)*GetOneGaussianByBoxMuller());
		double thisPayoff = final_S - Strike;
		sumPayOff += thisPayoff > 0 ? thisPayoff : 0;
	 
	}
	double expectedPayOff = sumPayOff/NumberOfPaths;
	expectedPayOff *= exp(-r*Expiry)

	return expectedPayOff;
}