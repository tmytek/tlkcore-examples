// ConsoleApplication1.cpp : 此檔案包含 'main' 函式。程式會於該處開始執行及結束執行。
//
//#define MULTIPLEBBOXONE
#include "stdio.h"
#include "pch.h"
#include <iostream>
#include <string>
#include <array>
#include <msclr/marshal.h>        // .NET string to C-style string
#include <msclr/marshal_cppstd.h> // .NET string to STL string
using namespace System;
using namespace BBoxAPI;
using namespace msclr::interop;

enum class TRMODE
{
	TX = 0,
	RX = 1,
};

int main()
{
	BBoxOneAPI ^b = gcnew BBoxOneAPI();

	//array<String ^>^ strarray = b->getStringArray();

	//array<String^>^ strarray = gcnew array<String^>(2);
	//for (int i = 0; i < 2; i++)
	//	strarray[i] = String::Concat("Number ", i.ToString());

	//for (int i = 0; i < strarray->Length; i++)
	//	Console::WriteLine("aa" + strarray[i]);

	//String^ net_s = "Hello .NET";
	//std::string nodename[2] = {"001", "110"}; // uses STL string, not .NET String
	//std::cout<< nodename[0]+"\n";
	//
	//marshal_context^ context = gcnew marshal_context();
	//const char* c_s = context->marshal_as<const char*>(net_s);
	//std::cout << c_s;
	////printf("%s\n", c_s);

	array<String ^>^ dev_info = b->ScanningDevice();

	for (int i = 0; i < dev_info->Length; i++)
		Console::WriteLine("device info from API side : " + dev_info[i]);


	/* It will send the init command to BBox. */
	/* first BBoxOne */
	String^  s_info_1 = b->Init("B19312200-24", 0);

	Console::WriteLine(s_info_1);
	Console::WriteLine("Init first one");

	int dev_1_spacing = b->selectAntenna(Device::AntennaType::FOURBYFOUR, 0);
	Console::WriteLine("1st device antenna spacing : " + dev_1_spacing);
	b->SwitchTxRxMode((int)TRMODE::TX, 0);


#if MULTIPLEBBOXONE
	/* second BBoxOne */
	String^  s_info_2 = b->Init("B19312300-24", 1);

	Console::WriteLine(s_info_2);
	Console::WriteLine("Init second one");

	int dev_2_spacing = b->selectAntenna(Device::AntennaType::FOURBYFOUR, 0);
	Console::WriteLine("2nd device antenna spacing : " + dev_2_spacing);
	b->SwitchTxRxMode((int)TRMODE::TX, 1);
	
#endif 
	Console::WriteLine("press enter to continue....");
	Console::Read();

	int deg = 0;
	int dir = -1;
	for (int count = 0; count < 1000; count++)
	{
		try
		{
			s_info_1 = b->setBeamX(5/*dB*/, deg/*degree*/, 0);
			s_info_1 = b->setBeamY(5/*dB*/, deg/*degree*/, 0);
			s_info_1 = b->setBeamXY(5/*dB*/, deg/*degree*/, deg/*degree*/, 0);
			Console::WriteLine("Firsr Device control : " + s_info_1);
#if MULTIPLEBBOXONE

			s_info_2 = b.setBeamX(0, deg, 1);
			s_info_2 = b.setBeamY(0, deg, 1);
			s_info_2 = b.setBeamXY(0, deg, deg, 1);
			Console::WriteLine("Second Device control : " + s_info_2);
#endif

			if (deg <= -25)
				dir = 1;
			else if (deg >= 25)
				dir = -1;
			deg += dir;
		}
		catch (...)
		{
			Console::WriteLine("An error occurred.");
		}
	}


	Console::Read();



}

// 執行程式: Ctrl + F5 或 [偵錯] > [啟動但不偵錯] 功能表
// 偵錯程式: F5 或 [偵錯] > [啟動偵錯] 功能表

// 開始使用的秘訣: 
//   1. 使用 [方案總管] 視窗，新增/管理檔案
//   2. 使用 [Team Explorer] 視窗，連線到原始檔控制
//   3. 使用 [輸出] 視窗，參閱組建輸出與其他訊息
//   4. 使用 [錯誤清單] 視窗，檢視錯誤
//   5. 前往 [專案] > [新增項目]，建立新的程式碼檔案，或是前往 [專案] > [新增現有項目]，將現有程式碼檔案新增至專案
//   6. 之後要再次開啟此專案時，請前往 [檔案] > [開啟] > [專案]，然後選取 .sln 檔案
