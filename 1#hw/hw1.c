#include <stdio.h>
#include <stdlib.h>

int main(){
  FILE *fd = fopen("pic.ppm","w");
  fprintf(fd,"P3\n%d %d\n%d\n",500,500,255);
  int x,y;
  double r,g,b;
  for(y = 0;y < 500;y++){
    r = 250 - (y*(.5));
    g = 0;
    b = 0;
    for(x = 0;x< 500;x++){
      r = r - ((250-(y*.5))/500);
      b = b + ((250-(y*.5))/500);
      fprintf(fd,"%d %d %d ",(int)r,(int)g,(int)b);
    }
  }
  fclose(fd);
}
