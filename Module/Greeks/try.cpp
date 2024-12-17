#include "./PartialDerivatives.h"
#include <iostream>
#include <tuple>
#include <functional> 
using namespace std;

class abs_class
{	
	public:
		abs_class(){}
		virtual ~abs_class(){}

		virtual double value(double a, double b) const = 0;
		double attr2 ;
		double attr1 ;
};

class der : public abs_class
{	
	public:
		der(double attr1_, double attr2_){
			attr1 = attr1_;
			attr2 = attr2_;
		}
		~der(){}

		double value(double a =0 , double b = 0) const 
		{	
			if (a == 0)  a = attr1;
			if (b == 0) {b = attr2;}
			return a*a+b*b ;

		}
};

class Greeks {
	public:
		Greeks( abs_class* obj_) : obj(obj_)
		{	
		step_size = 1.e-3;
		params = {obj->attr1,obj->attr2};
		//auto func1 = [this](double a, double b) {
		//		return PayOffObject->value(a,b);
		//	};
		//PartialDerivatives<decltype( func1) ,double, double, double, double > pd( func1, step_size);

 		}
		~Greeks(){
			//delete PayOffObject;
		};

		double step_size;
		double Delta()  const
		{	
			
			//auto func1 = [this](double a, double b) {
			//	return obj->value(a,b);
			//};
			//auto func1 = PayOffObject->value;
			//auto func2 = &(PayOffObject.value) ;
			//PartialDerivatives<decltype(func1),double, double > DerivativeObject( func1, step_size);
			PartialDerivatives<decltype(func1) ,double, double > pd( func1, step_size);
			//std::tuple<double,double> params = { 3.,4. };
			double ciccio = pd.second_compute<1>(params) ;

			cout<< ciccio << endl;
			return ciccio;	
		}
	private:
		abs_class* obj;
		std::tuple<double,double> params;
		static auto func1 = [abs_class* obj](double a, double b) {
				return obj->value(a,b);};
		//PartialDerivatives< decltype(Func), double ,double> pd(Func, step_size);
		//PartialDerivatives< decltype(func) ,double, double> pd(func, step_size);

};


int main()
{	

	der d_obj(3,4);

	der* pointer = &d_obj;
	Greeks g(pointer);
	cout << g.Delta() << endl;

	auto func1  = [](double a, double b) -> double{
				return a*a+b*b;
			};
    // Create a PartialDerivatives object with function `func` and step size 0.001
    PartialDerivatives<decltype(func1), double, double> partial_derivatives(func1, 0.001);

    std::tuple<double, double> paramss = {3.0, 4.0};  // Example point (x=3, y=4)

    // Compute the first partial derivative with respect to x (I=0)
    double first_derivative = partial_derivatives.first_compute<1>(paramss, 'C');
    std::cout << "First partial derivative wrt x: " << first_derivative << std::endl;

    return 0;
}


