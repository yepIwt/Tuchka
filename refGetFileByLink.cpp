#include<tchar.h>
#include<urlmon.h>

#pragma comment (lib,"urlmon.lib")

int main ()
{
  HRESULT hr=Urldownloadtofile( NULL, _T("http://"), _T("web_page.html") 0, NULL );

  return 0;
}