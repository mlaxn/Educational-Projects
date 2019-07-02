 //info
//directery is located at reserved size
#include <stdint.h>
#include <string.h>
#include <stdio.h>

FILE *fp;

short 	BPB_RsvdSecCnt;
short 	BPB_BytsPerSec;
int 	BPB_FATz32;
unsigned char 	BPB_SecPerClus;
unsigned char 	BPB_NumFATS;

int LBAToOffset(uint32_t sector){
    return (( sector-2) * BPB_BytsPerSec) +
            (BPB_BytsPerSec * BPB_RsvdSecCnt) +
            (BPB_NumFATS * BPB_FATz32 * BPB_BytsPerSec);
}

struct __attribute__((__packed__)) DirectoryEntry
{
    
    char DIR_Name[11];
    uint8_t Dir_Attr;
    uint8_t Unused1[8];
    uint16_t DIR_FirstClusterHigh;
    uint8_t Unused2[4];
    uint16_t DIR_FirstClusterLow;
    uint32_t DIR_FileSize;
};
struct DirectoryEntry dir[16];

int main ()
{
    //*************************************************************
    
    //info: prints the information of about te file
    
    fp= fopen("fat32.img","r");
    
printf(" ============================================ \n");

    fseek(fp, 11, SEEK_SET );
    fread(&BPB_BytsPerSec, 2, 1, fp);
    printf("BPB_BytsPerSec: %d\n",BPB_BytsPerSec);
    printf("BPB_BytsPerSec: %x\n",BPB_BytsPerSec);
    
    fseek(fp, 13, SEEK_SET );
    fread(&BPB_SecPerClus, 1, 1, fp);
    printf("BPB_SecPerClus:	%d\n",BPB_SecPerClus);
    printf("BPB_SecPerClus:	%x\n",BPB_SecPerClus);
    
    fseek(fp, 14, SEEK_SET );
    fread(&BPB_RsvdSecCnt, 2, 1, fp);
    printf("BPB_RsvdSecCnt:	%d\n",BPB_RsvdSecCnt);
    printf("BPB_RsvdSecCnt:	%x\n",BPB_RsvdSecCnt);
    
    fseek(fp, 16, SEEK_SET );
    fread(&BPB_NumFATS, 1, 1, fp);
    printf("BPB_NumFATS:	%d\n",BPB_NumFATS);
    printf("BPB_NumFATS:	%x\n",BPB_NumFATS);
    
    fseek(fp, 36, SEEK_SET );
    fread(&BPB_FATz32, 4, 1, fp);
    printf("BPB_FATz32:	%d\n",BPB_FATz32);
    printf("BPB_FATz32:	%x\n",BPB_FATz32);

    printf("\n");
    
    //***********************************************************
    
    
    
    //READ DIRECTORY
    //modify to read the
    int root_offset = (BPB_NumFATS * BPB_FATz32 * BPB_BytsPerSec) +
    (BPB_RsvdSecCnt * BPB_BytsPerSec);
    
    fseek(fp,root_offset,SEEK_SET);
    
   
    int i = 0;
    for(i=0; i<16; i++)
    {
        
        memset( &dir[i], 0, 3);
        //memset (&dir[i].DIR_Name, 0, 11);
        fread( &dir[i], 32, 1, fp);
    }
    
    for(i=0; i<16; i++)
    {
        if((dir[i].Dir_Attr == 0x10) || (dir[i].Dir_Attr == 0x20))
        {
            
            char name[12];
            memset( name, 0, 12);
            strncpy( name, dir[i].DIR_Name, 11);
            printf("%s   %d    %d\n", name, dir[i].DIR_FileSize, dir[i].DIR_FirstClusterLow); //TODO
        } //ls command
    }
    
    //***********************************************************************
    //read
    
    
     int file_offset = LBAToOffset( 17);
     
     fseek(fp, file_offset, SEEK_SET);
     uint8_t value;
     fread( &value, 1, 1, fp);
     
     printf("\nRead123: %d\n", value);
     
     //read NUM.txt 513 1
     int user_offset = 513;
     int block = 7216;
     
     while( user_offset > BPB_BytsPerSec)
     {
//        block = NextLb(block);
        user_offset -= BPB_BytsPerSec;
     }
     
     //block has the data
     file_offset = LBAToOffset( block);
     fseek(fp, file_offset + user_offset, SEEK_SET);
    
     for(i=1; i< user_offset; i++)
     {
         fread( &value, 1, 1, fp);
         printf("&d\n", value);
     }
    
printf(" ============================================\n ");
    fclose(fp);
    return 0;
    
}






