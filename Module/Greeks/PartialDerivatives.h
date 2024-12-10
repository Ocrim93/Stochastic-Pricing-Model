#ifndef PARTIALDERIVATIVES_H
#define PARTIALDERIVATIVES_H

#include <tuple>
#include <cmath>


template<typename Func, typename Tuple, std::size_t...I>
auto apply_impl(Func&& func, Tuple&& t, std::index_sequence<I...>)	
{
	return func(std::get<I>(std::forward<Tuple>(t))...);
}

template< typename Func, typename Tuple>
auto apply( Func&& func, Tuple&& t)
{
	constexpr auto size = std::tuple_size<std::decay_t<Tuple>>::value;
	return apply_impl(std::forward<Func>(func), std::forward<Tuple>(t), std::make_index_sequence<size>());
}

template<typename Func, typename Args> 
class PartialDerivatives {
	public:
		PartialDerivatives(Func func_, double step_size_) : func(func_), h(step_size_){}

		// function to compute the first partial derivative wrt i-th, std::get<I> needs an constant parameter at compile-time--> template
		template< std::size_t I>
		double first_compute(const std::tuple<Args...>& params, char method = 'C' ) const
		{
			auto params_forward = params;
			auto params_backward = params;
			double step_size = h;

			switch(method)
			{
				case 'C':
					std::get<I>(params_forward) += h;
					std::get<I>(params_backward) -= h;
					step_size = 2*h;
				case 'F':
					std::get<I>(params_forward) += h;
				case 'B':
					std::get<I>(params_backward) -= h;
			}
			double f_forward = apply(func,params_forward);
			double f_backward = apply(func,params_backward);

			return (f_forward - f_backward)/(step_size);

		}

		template< std::size_t I>
		double second_compute(const std::tuple<Args...>& params, char method = 'C' ) const
		{
			auto params_forward = params;
			auto params_backward = params;
			double step_size = h;

			std::get<I>(params_forward) += h;
			std::get<I>(params_backward) -= h;

			double f_forward = apply(func,params_forward);
			double f_backward = apply(func,params_backward);
			double f = apply(func,params);

			return (f_forward + f_backward - 2*f)/(pow(step_size,2));

		}

	private:
		Func func;
		double  h;

};

#endif