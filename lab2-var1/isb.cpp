#include <iostream>
#include <fstream>
#include <random>
#include <bitset>
#include <ctime>

using namespace std;

int main()
{

    unsigned seed = static_cast<unsigned>(time(nullptr));
    mt19937 generator(seed);
    uniform_int_distribution<int> dist(0, 1);


    bitset<128> bits;

    for (int i = 0; i < 128; ++i)
    {
        bits.set(i, dist(generator));
    }

    cout << "C++ GPSH (128 bit):\n" << bits << endl;

    ofstream output_file("bin_seq_cpp.txt");
    if (output_file.is_open())
    {
        output_file << bits;               // ���������� ������ � ����
        output_file.close();                // ��������� ����
        cout << "Sequence saved to bin_seq_cpp.txt." << endl;
    }
    else
    {
        cerr << "Error: Could not open the file for writing!" << endl;
        return 1;                          // ��������� ��������� � �������
    }

    return 0;
}
