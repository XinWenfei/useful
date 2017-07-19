#include<iostream>
using namespace std;

template <typename T>
class BaseClass{
    public:
        virtual double operator()(T arg) = 0;
};

template <typename T, typename ARG>
class Calculator : public BaseClass<ARG>{
    private:
        double (T::*m_pmi)(ARG arg);
        T* m_p;
    public:
        Calculator(T* p, double (T::*_pmi)(ARG arg)){
            m_p = p;
            m_pmi = _pmi;
        }

        virtual double operator()(ARG arg){
            (*m_p.*m_pmi)(arg);
        }
};

class Number{
    public:
        double a;
        Number(double a1):a(a1){cout<<"a = "<<a<<endl;}
        double Add(double b){
            cout<<"b = "<<b<<"  ";
            cout<<"a + b = "<<a+b<<endl;
            return a + b;
        }

        double Sub(double b){
            cout<<"b = "<<b<<"  ";
            cout<<"a - b = "<<a-b<<endl;
            return a - b;
        }

        double Mul(double b){
            cout<<"b = "<<b<<"  ";
            cout<<"a * b = "<<a*b<<endl;
            return a * b;
        }

        double Div(double b){
            cout<<"b = "<<b<<"  ";
            if(b!=0){
                cout<<"a / b = "<<a/b<<endl;
                return a / b;
            }else{
                cout<<"divisor can't be zero!"<<endl;
            }
        }
};

int main()
{
   Number number(10);
   Calculator<Number, double> add(&number, &Number::Add);
   Calculator<Number, double> sub(&number, &Number::Sub);
   Calculator<Number, double> mul(&number, &Number::Mul);
   Calculator<Number, double> div(&number, &Number::Div);
   add(5);
   sub(3);
   mul(2);
   div(5);
   div(0);

   return 0;
}
