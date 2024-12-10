#ifndef VANILLA_H
#define VANILLA_H

#include "../Payoff.cpp"

class VanillaCall : public PayOff{
	public:
		VanillaCall(double Strike_);
		VanillaCall(double Strike_, double Expiry_, double Spot_ ,double Vol_,double r_, double q_ );
		virtual ~VanillaCall(){}
		virtual PayOff* clone() const;
		virtual double operator()(double Spot) const;
		virtual double Value(double Expiry_ , double Spot_, double Vol_, double r_, double q_ ) const ;

		void SetNumberOfPaths(unsigned long NumberOfPaths_) ;

		unsigned long NumberOfPaths;

		double Expiry;
		double Spot;
		double Vol;
		double r;
		double q;
	private:
		double Strike;
		

};


#endif 