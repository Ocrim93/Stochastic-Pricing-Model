#ifndef VANILLA_H
#define VANILLA_H
#include "../Payoff.cpp"

class VanillaCall : public PayOff{
	public:
		VanillaCall(){};
		VanillaCall(double Strike_, double Expiry_, double Spot_ ,double Vol_,double r_, double q_ );
		virtual ~VanillaCall(){}
		virtual PayOff* clone() const;
		virtual double operator()(double Spot) const;
		virtual double Value(double Expiry_ , double Spot_, double Vol_, double r_ ) const ;

		void SetNumberOfPaths(unsigned long NumberOfPaths_) ;

		unsigned long NumberOfPaths;

	private:
		double Strike;
		double q;

};


#endif 