#include "Random.h"
#include <cstdlib>
#include  <cmath>

double GetOneGaussianByBoxMuller(){
	// rand() generates pseduo-random number between 0 and RAND_MAX
	// x, y need to be [-1,1]

	double gaussianVariable;
	double x;
	double y;

	double radiusSquared;
	do{
		x = 2.0*rand()/static_cast<double>(RAND_MAX) -1;
		y = 2.0*rand()/static_cast<double>(RAND_MAX) -1;
		radiusSquared = x*x + y*y;
	}while(radiusSquared >=1);

	gaussianVariable = x*sqrt(-2*log(radiusSquared)/radiusSquared);

	return gaussianVariable;
}