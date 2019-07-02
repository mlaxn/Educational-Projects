#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <signal.h>
#include <stdint.h>
#include <ctype.h>
#define WHITESPACE " \t\n"
#define MAX_COMMAND_SIZE 255

// Mav shell only supports ten arguments

#define MAX_NUM_ARGUMENTS 10

struct __attribute__ ((__packed__)) DirectoryEntry

{

    char DIR_NAME[11];
    uint8_t DIRAttr;
    uint8_t Unused1[8];
    uint16_t DIR_FirstClusterHigh;
    uint8_t Unused2[4];
    uint16_t DIR_FirstClusterLow;
    uint32_t DIR_FileSize;

};


struct dirEnt *dp;

int32_t RootDirSectors = 0;
int32_t FirstDataSector = 0;
int32_t FirstSectorofCluster = 0;

int16_t BPB_BytesPerSec;
int8_t BPB_SecPerClus;
int16_t BPB_RsvdSecCnt;
int8_t BPB_NumFATs;
int32_t BPB_FATSz32;

int16_t val;
int8_t val2;
int32_t val3;
int16_t val4;
int8_t val5;
char  val6;
FILE * fp;

int16_t NextLB( uint32_t sector)
{
    uint32_t FATAddress = (BPB_BytesPerSec * BPB_RsvdSecCnt) + ( sector*4);
    uint16_t val;
    fseek( fp, FATAddress, SEEK_SET);
    fread( &val, 2, 1, fp);
    return val;
}

struct DirectoryEntry dir[16];

int LBAToOffset( uint16_t DIR_FirstClusterLow )

{
        return ( ( DIR_FirstClusterLow - 2 ) * val ) + ( val * val4 ) + ( val * val5 * val3 );
}

void read_file(char * filename, int length, int offset)
{
    int sec_count = (int) offset/512;
    int i;
    char byte;

    // search the directory and find the entry that matches filename
    // set ssector to DIR_FirstClusterLow

    int firstclusterlow;
    int a , b;
    a = strlen(filename);
    b = strlen(dir[8].DIR_NAME);
    char temp[11];
    temp[11] = '\0';
    strncpy( temp, "           ", 11 );

    char * tok = strtok( filename, "." );
    strncpy( temp, tok, strlen(tok) );

    tok = strtok( NULL, "." );

    if (tok  != NULL)
        strncpy( &temp, tok, 3 );

    for( i = 0; i < strlen(temp); i++ )
    {
        temp[i] = toupper( temp[i] );
    }

    for(i=0;i<16;i++)
    {
        if(strncmp(dir[i].DIR_NAME,temp,11)==0)
        {
            firstclusterlow = dir[i].DIR_FirstClusterLow;
        }
        for(i = 0; i<sec_count; i++)
        {
            offset = offset %512;
            firstclusterlow = NextLB(firstclusterlow);
        }
        int file_offset = LBAToOffset (firstclusterlow);

        fseek(fp, offset + file_offset, SEEK_SET);
        if((offset + length)>512)
        {
            int count = 512 - offset;
            for (i=0 ; i<count; i++)
            {
                fread(&byte, 1, 1, fp);
                printf("%x", byte);
            }
            int NB = NextLB(firstclusterlow);
            file_offset = LBAToOffset(NB);
            fseek(fp, file_offset, SEEK_SET);
            count = length - count;
            for (i=0 ; i<count; i++)
            {
                fread(&byte, 1, 1, fp);
                printf("%x", byte);
            }
        }
        else
        {
            for (i=0; i<length; i++)
            {
                fread(&byte,1,1,fp);
                printf("%x");
            }
            printf("\n");
        }
    }
}

int main ()
{
    char * cmd_str = (char*) malloc( MAX_COMMAND_SIZE );
    char *path1, *path2, *path3, *path4;

    //allocating memory to 4 paths
    path1 = (char *)malloc(MAX_COMMAND_SIZE);
    path2 = (char *)malloc(MAX_COMMAND_SIZE);
    path3 = (char *)malloc(MAX_COMMAND_SIZE);
    path4 = (char *)malloc(MAX_COMMAND_SIZE);

    //copies to first n characters of max_command_size
    memset(path1,0,MAX_COMMAND_SIZE);
    memset(path2,0,MAX_COMMAND_SIZE);
    memset(path3,0,MAX_COMMAND_SIZE);
    memset(path4,0,MAX_COMMAND_SIZE);

    //copies string to paths
    strcpy(path1,"./");
    strcpy(path2,"/usr/local/bin/");
    strcpy(path3, "/usr/bin/");
    strcpy(path4, "/bin/");

    int count=0;
    int x;
    int pid[10];
    int closeCheck = 0;

    while (1)
    {
        printf ("mfs>");

        // Read the command from the commandline.
        //The maximum command that will be read is MAX_COMMAND_SIZE
        // This while command will wait here until the user
        // inputs something since fgets returns NULL when there
        // is no input

        while( !fgets (cmd_str, MAX_COMMAND_SIZE, stdin) );
        /* Parse input */

        char *token[MAX_NUM_ARGUMENTS];
        int   token_count = 0;
        // Pointer to point to the token
        // parsed by strsep

        char *arg_ptr;
        char *working_str  = strdup( cmd_str );

        // we are going to move the working_str pointer so
        // keep track of its original value so we can deallocate
        // the correct amount at the end
        char *working_root = working_str;

        // Tokenize the input stringswith whitespace used as the delimiter

        while ( ( (arg_ptr = strsep(&working_str, WHITESPACE ) ) != NULL) &&
               (token_count<MAX_NUM_ARGUMENTS))
        {
            token[token_count] = strndup( arg_ptr, MAX_COMMAND_SIZE );
            if( strlen( token[token_count] ) == 0 )
            {
                token[token_count] = NULL;
            }
            token_count++;
        }

        if(token[0] == NULL)
        {
        }

        else if(strcmp (token[0], "open") == 0 && token[1] == NULL)
        {
            printf("Please enter the filename along with open command.\n");
        }

        else if(strcmp (token[0], "open") == 0 && strcmp (token[1], "fat32.img") == 0)
        {
            //printf("%S", token[1]);
            fp = fopen ("fat32.img", "r");
            if (fp == NULL)
            {
                printf("Error: File system image not found.\n");
            }

            else {
                closeCheck = 1;
                int i;
                fseek (fp, 11, SEEK_SET);
                fread (&val, 2, 1, fp);
                fread (&val2, 1, 1, fp);
                fread (&val4, 2, 1, fp);
                fread (&val5, 1, 1, fp);
                fseek(fp, 36, SEEK_SET);
                fread (&val3, 2, 2, fp);
                fseek(fp, 0x100400, SEEK_SET);

                for (i=0; i<16; i++)
                {
                    fread(dir[i].DIR_NAME, 11, 1, fp);
                    //dir[i].DIR_NAME[11] = '\0';
                    fread(&dir[i].DIRAttr,1,1,fp );
                    fread(&dir[i].Unused1, 8,1,fp);
                    fread(&dir[i].DIR_FirstClusterHigh,2,1,fp);
                    fread(&dir[i].Unused2,4,1,fp);
                    fread(&dir[i].DIR_FirstClusterLow,2,1,fp);
                    fread(&dir[i].DIR_FileSize, 4, 1,fp);
                }
            }
        }

        else if(strcmp (token[0], "open") == 0 && strcmp (token[1], "fat32.img") != 0)
        {
            printf("File does not exist.\n");
        }

        else if(strcmp (token[0], "close") == 0 && token[1] == NULL)
        {
            printf("Please enter the filename along with close command.\n");
        }
        else if (strcmp (token[0], "close") == 0 && strcmp (token[1], "fat32.img") == 0)
        {
            if(closeCheck == 1){
                closeCheck = fclose(fp);
                if(fp  == NULL)
                {
                    printf("Error: File system not open.\n");
                }
            }
            else
            {
                printf("File must be opened first.\n");
            }
        }
        else if(strcmp (token[0], "close") == 0 && strcmp (token[1], "fat32.img") != 0)
        {
            printf("File does not exist.\n");
        }

        else if (strcmp (token[0], "info") == 0)
        {
            if(closeCheck != 0){
                printf("Information in hexadecimal and base 10: \n");
                printf("BRB_BytesPerSec: %x %d\n", val, val);
                printf("BPB_SecPerClus : %x %d\n", val2, val2);
                printf("BPB_RsvdSecCnt: %x  %d\n", val4, val4);
                printf("BPB_NumFATs: %x %d\n", val5, val5);
                printf("BPB_FATSz32: %x %d\n", val3, val3);
            }
            else
            {
                printf("file system image must be opened first.\n");
            }
        }

        else if(strcmp (token[0], "stat") == 0 && token[1] == NULL)
        {
            printf("Please enter the filename along with stat command.\n");
        }
        else if (strcmp (token[0], "stat") == 0 && token[1] != NULL)
        {
            if(closeCheck != 0)
            {
                int index;
                char * string = (char*)malloc(12);
                for(index = 0; index <16; index ++)
                {
                    memset (string, '\0', 12);
                    strcpy(string, token[1]);
                    char * directory_string;

                    // You will get this from the directory
                    directory_string = (char*) malloc ( 11 );
                    strncpy( directory_string, dir[index].DIR_NAME, 11 );

                    // You will get this from the user
                    char * user_input;

                    user_input  = (char*) malloc ( 11 );
                    strncpy( user_input, string, 11 );

                    char temp_string[12];

                    // Null terminate and fill with spaces
                    memset( temp_string,  0, 12 );
                    strncpy( temp_string, "           ", 11 );

                    // Parse the filename into two tokens using the
                    // period as the delimiter
                    char * token = strtok( user_input, "." );

                    // Copy the filename
                    strncpy( temp_string, token, strlen(token) );

                    // Parse the 3 letter extension
                    token = strtok( NULL, "." );
                    if (token != NULL)
                        // Copy the filename
                    {strncpy( &temp_string[8], token, 3 );}

                    int i;
                    for( i = 0; i < strlen(temp_string); i++ )
                    {
                        temp_string[i] = toupper( temp_string[i] );
                    }

                    if( strcmp( temp_string, directory_string ) == 0 )
                    {
                        printf (" %s\t Attr:%d\t Low:%d\t Size:%d\n", dir[index].DIR_NAME,
                            dir[index].DIRAttr,  dir[index].DIR_FirstClusterLow,
                            dir[index].DIR_FileSize );
                        break;
                    }
                }
            }
            else
            {
                printf("file system image must be opened first.\n");
            }
        }

        else if (strcmp (token[0], "ls") == 0)
        {
            if(closeCheck == 1){
                int i;
                for ( i=0; i<16; i++)
                {
                    char * str = (char*) malloc(12);
                    memset (str, 0, 12);
                    strncpy (str, dir[i].DIR_NAME,11);
                    if ((dir[i].DIRAttr==1) || (dir[i].DIRAttr ==16) || (dir[i].DIRAttr ==32))
                    {
                        if ((int)dir[i].DIR_NAME[0] !=229)
                            printf("%s %d \n", str, dir[i].DIR_FileSize);
                    }
                }
            }
            else
            {
                printf("file system image must be opened first.\n");
            }
        }

        else if (strcmp (token[0], "cd") == 0 && token[1] != NULL)
        {
            if(closeCheck == 1){
                int firstclusterlow;
                int a , b;
                a = strlen(token[1]);
                b = strlen(dir[8].DIR_NAME);
                char temp[11];
                temp[11] = '\0';
                strncpy( temp, "           ", 11 );

                char * tok = strtok( token[1], "." );
                strncpy( temp, tok, strlen(tok) );

                tok = strtok( NULL, "." );

                if (tok  != NULL)
                    strncpy( &temp, tok, 3 );

                int i;
                for( i = 0; i < strlen(temp); i++ )
                {
                    temp[i] = toupper( temp[i] );
                }

                for(i=0;i<16;i++)
                {
                    if(strncmp(dir[i].DIR_NAME,temp,11)==0)
                    {
                        firstclusterlow = dir[i].DIR_FirstClusterLow;
                    }
                }
                int file_offset = LBAToOffset( firstclusterlow );
                fseek(fp, file_offset, SEEK_SET);

                for (i=0 ; i<16; i++)

                {
                    fread(&dir[i], 32,1, fp);

                }
            }
            else
            {
                printf("file system image must be opened first.\n");
            }

        }
        else if (strcmp (token[0], "cd") == 0 && token[1] == NULL)
        {
            printf("Please enter path.\n");
        }
        else if (strcmp(token[0], "read") == 0 )
        {
            if(closeCheck == 1)
            {
                char * filename = token[1];
                int * length = token[2];
                int * offset = token[3];
                read_file( filename, length, offset);
            }
            else
            {
                printf("file system image must be opened first.\n");
            }
        }

        else if (strcmp (token[0], "volume") == 0)
        {
            
            if(closeCheck == 1){
                fseek (fp, 43, SEEK_SET);
                fread (&val6, 11, 1, fp);
                printf("Volume:%c\n", val6);
            }
            else
            {
                printf("file system image must be opened first.\n");
            }
        }
    }
}
