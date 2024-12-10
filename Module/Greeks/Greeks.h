#ifndef GREEKS_H
#define GREEKS_H
#include "./PartialDerivatives.h"

template<typename PayOff_T>
class Greeks {
	public:
		Greeks( const PayOff_T& PayOff_){}
		~Greeks(){}
		double Delta() const;
		//double Vega() const;
		//double Gamma() const;
		//double Rho() const;

	private:
		PayOff_T PayOffObject;
		PartialDerivatives DerivativeObject; 

};

#endif GREEKS_H