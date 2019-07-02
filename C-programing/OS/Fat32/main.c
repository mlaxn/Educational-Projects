/*
 Milan Biswakarma
 Santosh Nepal
 CSE 3320-002
 Lab 3 FAT32 File System
 December 6, 2017
 */

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
#define MAX_NUM_ARGUMENTS 10

struct __attribute__ ((__packed__)) DirectoryEntry {
    char DIR_Name[11];
    uint8_t DIR_Attr;
    uint8_t Unused1[8];
    uint16_t DIR_FirstClusterHigh;
    uint8_t Unused2[4];
    uint16_t DIR_FirstClusterLow;
    uint32_t DIR_FileSize;
    
};
struct DirectoryEntry dir[16];

struct dirEnt *dp;

int32_t RootDirSectors = 0;
int32_t FirstDataSector = 0;
int32_t FirstSectorofCluster = 0;

int16_t BPB_BytesPerSec;
int8_t BPB_SecPerClus;
int16_t BPB_RsvdSecCnt;
int8_t BPB_NumFATs;
int32_t BPB_FATSz32;

int16_t value_BytesPerSec;
int8_t value_SecPerClus;
int32_t value_FatSz32;
int16_t value_RsvdSecCnt;
int8_t value_NumFATs;
char value_volume;

FILE * fp;

int16_t NextLB(uint32_t sector) {
    uint32_t FATAddress = (BPB_BytesPerSec * BPB_RsvdSecCnt) + (sector * 4);
    uint16_t val;
    fseek(fp, FATAddress, SEEK_SET);
    fread(&val, 2, 1, fp);
    return val;
}

int LBAToOffset(uint16_t DIR_FirstClusterLow) {
    return ( (DIR_FirstClusterLow - 2) * BPB_BytesPerSec) +
    (BPB_BytesPerSec * BPB_RsvdSecCnt) +
    (BPB_BytesPerSec * BPB_NumFATs * BPB_FATSz32);
}

void readFileDirectory(char* filename, int length, int offset) {
    
    int sectorCounter = (int) offset / 512;
    int value_firstclusterlow;
    char value_byte;
    int i;
    
    char temp[12];
    temp[11] = '\0';
    strncpy(temp, "           ", 11);
    
    char * tok = strtok(filename, ".");
    strncpy(temp, tok, strlen(tok));
    tok = strtok(NULL, ".");
    
    if (tok != NULL)
        strncpy(temp, tok, 3);
    
    for (i = 0; i < strlen(temp); i++) {
        temp[i] = toupper(temp[i]);
    }
    
    for (i = 0; i < 16; i++) {
        if (strncmp(dir[i].DIR_Name, temp, 11) == 0) {
            value_firstclusterlow = dir[i].DIR_FirstClusterLow;
        }
        for (i = 0; i < sectorCounter; i++) {
            offset = offset % 512;
            value_firstclusterlow = NextLB(value_firstclusterlow);
        }
        int file_offset = LBAToOffset(value_firstclusterlow);
        
        fseek(fp, offset + file_offset, SEEK_SET);
        if ((offset + length) > 512) {
            int index = 512 - offset;
            for (i = 0; i < index; i++) {
                fread(&value_byte, 1, 1, fp);
                printf("%x", value_byte);
            }
            int NB = NextLB(value_firstclusterlow);
            file_offset = LBAToOffset(NB);
            fseek(fp, file_offset, SEEK_SET);
            index = length - index;
            for (i = 0; i < index; i++) {
                fread(&value_byte, 1, 1, fp);
                printf("%x", value_byte);
            }
        } else {
            for (i = 0; i < length; i++) {
                fread(&value_byte, 1, 1, fp);
            }
            printf("\n");
        }
    }
}

int main() 
{
    
    int fileCheckBool = 0;
    int counter = 0;
    int x;
    
    char * cmd_str = (char*) malloc(MAX_COMMAND_SIZE);
    
    while (1) {
        printf("\nmfs>");
        
        // Read the command from the commandline.
        //The maximum command that will be read is MAX_COMMAND_SIZE
        // This while command will wait here until the user
        // inputs something since fgets returns NULL when there
        // is no input
        
        while (!fgets(cmd_str, MAX_COMMAND_SIZE, stdin));
        /* Parse input */
        
        char *token[MAX_NUM_ARGUMENTS];
        int token_count = 0;
        // Pointer to point to the token
        // parsed by strsep
        
        char *arg_ptr;
        char *working_str = strdup(cmd_str);
        
        // we are going to move the working_str pointer so
        // keep track of its original value so we can deallocate
        // the correct amount at the end
        char *working_root = working_str;
        
        // Tokenize the input stringswith whitespace used as the delimiter
        
        while (((arg_ptr = strsep(&working_str, WHITESPACE)) != NULL) &&
               (token_count < MAX_NUM_ARGUMENTS)) {
            token[token_count] = strndup(arg_ptr, MAX_COMMAND_SIZE);
            if (strlen(token[token_count]) == 0) {
                token[token_count] = NULL;
            }
            token_count++;
        }
        
        //========================================================================================================
        if (token[0] == NULL) {
            continue;
        }
        if (strcmp(token[0], "exit") == 0 || strcmp(token[0], "quit") == 0) {
            exit(0);
        }//========================================================================================================
        else if (strcmp(token[0], "open") == 0) {
            if (token[1] == NULL) {
                printf("Error: File name must be entered in format open <filename>.\n");
            } else if (strcmp(token[1], "fat32.img") == 0) {
                fp = fopen("fat32.img", "r");
                if (fp == NULL) {
                    printf("Error: File system image not found.\n");
                }
                if (fileCheckBool == 1) {
                    printf("Error: File system image already open.\n");
                    
                } else {
                    fileCheckBool = 1;
                    int i;
                    fseek(fp, 11, SEEK_SET);
                    fread(&value_BytesPerSec, 2, 1, fp);
                    fread(&value_SecPerClus, 1, 1, fp);
                    fread(&value_RsvdSecCnt, 2, 1, fp);
                    fread(&value_NumFATs, 1, 1, fp);
                    fseek(fp, 36, SEEK_SET);
                    fread(&value_FatSz32, 2, 2, fp);
                    fseek(fp, 0x100400, SEEK_SET);
                    
                    for (i = 0; i < 16; i++) {
                        fread(dir[i].DIR_Name, 11, 1, fp);
                        fread(&dir[i].DIR_Attr, 1, 1, fp);
                        fread(&dir[i].Unused1, 8, 1, fp);
                        fread(&dir[i].DIR_FirstClusterHigh, 2, 1, fp);
                        fread(&dir[i].Unused2, 4, 1, fp);
                        fread(&dir[i].DIR_FirstClusterLow, 2, 1, fp);
                        fread(&dir[i].DIR_FileSize, 4, 1, fp);
                    }
                }
                
            } else {
                printf("Error:File system image not found.\n");
            }
            
        }            //======================================================================================================
        else if (strcmp(token[0], "close") == 0) {
            if (token[1] == NULL) {
                printf("File name must be entered in format close <filename>.\n");
            } else if (strcmp(token[1], "fat32.img") == 0) {
                if (fileCheckBool == 1) {
                    fileCheckBool = fclose(fp);
                    if (fp == NULL) {
                        printf("Error: File system not open.\n");
                    }
                } else {
                    printf("Error: File system image must be opened first.\n");
                }
            } else {
                printf("Error: File does not exist.\n");
            }
        }            //======================================================================================================
        else if (strcmp(token[0], "info") == 0) {
            if (fileCheckBool == 1) {
                printf("Information in Hexadecimal and Base 10 respectively: \n");
                printf("BRB_BytesPerSec: %d\n", value_BytesPerSec);
                printf("BRB_BytesPerSec: %x\n", value_BytesPerSec);
                
                printf("BPB_SecPerClus : %d\n", value_SecPerClus);
                printf("BPB_SecPerClus : %x\n", value_SecPerClus);
                
                printf("BPB_RsvdSecCnt: %d\n", value_RsvdSecCnt);
                printf("BPB_RsvdSecCnt: %x\n", value_RsvdSecCnt);
                
                printf("BPB_NumFATs: %d\n", value_NumFATs);
                printf("BPB_NumFATs: %x\n", value_NumFATs);
                
                printf("BPB_FATSz32: %d\n", value_FatSz32);
                printf("BPB_FATSz32: %x\n", value_FatSz32);
            } else {
                printf("Error: File system image must be opened first.\n");
            }
        }            //============================================================================================
        else if (strcmp(token[0], "stat") == 0) {
            if (token[1] == NULL) {
                printf("Error: Enter the filename along with stat command.\n");
            } else {
                if (fileCheckBool != 0) {
                    int index;
                    char * text = (char*) malloc(12);
                    
                    for (index = 0; index < 16; index++) {
                        memset(text, '\0', 12);
                        strcpy(text, token[1]);
                        
                        char * input;
                        char * text_path;
                        char temp_string[12];
                        text_path = (char*) malloc(11);
                        input = (char*) malloc(11);
                        
                        strncpy(text_path, dir[index].DIR_Name, 11);
                        strncpy(input, text, 11);
                        
                        memset(temp_string, 0, 12);
                        strncpy(temp_string, "           ", 11);
                        
                        char * token = strtok(input, ".");
                        
                        strncpy(temp_string, token, strlen(token));
                        
                        token = strtok(NULL, ".");
                        if (token != NULL) {
                            strncpy(&temp_string[8], token, 3);
                        }
                        
                        int i;
                        for (i = 0; i < strlen(temp_string); i++) {
                            temp_string[i] = toupper(temp_string[i]);
                        }
                        
                        if (strcmp(temp_string, text_path) == 0) {
                            printf(" %s\n Attr:%d\n Low:%d\n Size:%d\n", dir[index].DIR_Name,
                                   dir[index].DIR_Attr, dir[index].DIR_FirstClusterLow,
                                   dir[index].DIR_FileSize);
                            break;
                        }
                    }
                } else {
                    printf("Error: File system image must be opened first.\n");
                }
            }
        }            //=====================================================================================================
        else if (strcmp(token[0], "cd") == 0) {
            if (token[1] != NULL) {
                if (fileCheckBool == 1) {
                    
                    int firstclusterlowNum;
                    char temp[12];
                    temp[11] = '\0';
                    strncpy(temp, "           ", 11);
                    
                    char * tok = strtok(token[1], ".");
                    strncpy(temp, tok, strlen(tok));
                    
                    tok = strtok(NULL, ".");
                    if (tok != NULL)
                        strncpy(&temp, tok, 3);
                    
                    int i;
                    for (i = 0; i < strlen(temp); i++) {
                        temp[i] = toupper(temp[i]);
                    }
                    
                    for (i = 0; i < 16; i++) {
                        if (strncmp(dir[i].DIR_Name, temp, 11) == 0) {
                            firstclusterlowNum = dir[i].DIR_FirstClusterLow;
                        }
                    }
                    int file_offset = LBAToOffset(firstclusterlowNum);
                    fseek(fp, file_offset, SEEK_SET);
                    
                    for (i = 0; i < 16; i++) {
                        fread(&dir[i], 32, 1, fp);
                        
                    }
                } else {
                    printf("Error: File system image must be opened first.\n");
                }
            } else if (strcmp(token[1], "..") == 0) {
                
            } else {
                printf("Error: Enter path.\n");
            }
        }            //==================================================================================================
        else if (strcmp(token[0], "ls") == 0) {
            if (fileCheckBool == 1) {
                int i;
                for (i = 0; i < 16; i++) {
                    char * text = (char*) malloc(12);
                    memset(text, 0, 12);
                    strncpy(text, dir[i].DIR_Name, 11);
                    if (((dir[i].DIR_Attr == 1) || (dir[i].DIR_Attr == 16) || (dir[i].DIR_Attr == 32))
                        && (int) dir[i].DIR_Name[0] != 229) {
                        printf("%s %d \n", text, dir[i].DIR_FileSize);
                    }
                }
            } else {
                printf("Error: File system image must be opened first.\n");
            }
        }            //===================================================================================================
        
        /*  else if (strcmp(token[0], "read") == 0) {
         if (closeCheck == 1) {
         char * filename = token[1];
         int* length = token[2];
         int * offset = token[3];
         
         readFileDirectory(filename, length, offset);
         
         int offset_real = LBAToOffset(length);
         fseek(fp,offset_real,SEEK_SET);
         int i;
         for(i=0; i<16; i++){
         fread(&filename,32,1,fp);
         }
         
         
         } else {
         printf("Error: File system image must be opened first.\n");
         }
         }
         */
        //*******************************************
        else if (strcmp(token[0], "read") == 0) {
            if (fileCheckBool == 1) {
                char* filename = token[1];
                int length  = atoi(token[2]);
                int  offset = atoi (token[3]);
               // int* length = token[2];
               // int* offset = token[3];
                
                uint8_t value;
                fread(&value, 1, 1, fp);
                printf("\nRead: %d\n", value);
                
                //calculate the cluster number  using the file name
                int clusterNum = 0;
                int i;
                for (i = 0; i < 16; i++) {
                    if (strncmp(dir[i].DIR_Name, filename, 11) == 0) {
                        clusterNum = dir[i].DIR_FirstClusterLow;
                    }
                }
                    int file_offset = LBAToOffset(clusterNum);
                    int user_offset = length;
                    int block = dir[clusterNum].DIR_FirstClusterLow;
                    
                    while (user_offset > BPB_BytesPerSec) {
                        user_offset -= BPB_BytesPerSec;
                    }
                    file_offset = LBAToOffset(block);
                    fseek(fp, file_offset + user_offset, SEEK_SET);
                    
                    for (i = 1; i< user_offset; i++) {
                        //readFileDirectory( filename, length, offset);
                        fread(&value, 1,1, fp);
                        printf("\nRead: %d\n", value);
                        break;
                    }
                }
            else {
                    printf("Error: File system image must be opened first.\n");
                }
            }
        
            //==================================================================================================
            
            else if (strcmp(token[0],"volume") == 0) {
                if (fileCheckBool == 1) {
                    fseek(fp,71, SEEK_SET);
                    fread(&value_volume, 11, 1, fp);
                    printf("Volume:%c\n", value_volume);
                }
                else {
                    printf("file system image must be opened first.\n");
                }
            }
            //==================================================================================================
            /*
             else if (strcmp(token[0], "get") == 0) {
             
             int i;
             if (closeCheck == 1) {
             for (i = 0; i < 16; i++) {
             int size = dir[i].DIR_FileSize;
             i
             cluster = dir[i].DIR_FirstClusterLow;
             fseek(fp, LBAToOffset(dir[i].DIR_FirstClusterLow, SEEK_SET));
             
             while (size > 512) {
             fread(, 512,);
             fwrite
             size = size - 512;
             culster = NextLB();
             }
             fseek();
             fread();
             
             }
             }
             }
             */
            
            //=================================================================================================
            
            else {
                printf("Error: Command Not Recognized.\nTry Again !!!");
            }
            
            free(working_root);
        }
        
        return 0;
    }
    
/*
 * 
 * else if (strcmp(token[0], "stat") == 0)
        {
            if (token[1] == NULL)
            {
                printf("Error: Enter the filename along with stat command.\n");
            }
            else
            {
                if (fileCheckBool != 0)
                {
                    int index;
                    char * text = (char*) malloc(12);
                    
                    for (index = 0; index < 16; index++) {
                        memset(text, '\0', 12);
                        strcpy(text, token[1]);
                        
                        char * input;
                        char * text_path;
                        char temp_string[12];
                        text_path = (char*) malloc(12);
                        input = (char*) malloc(12);
                        
                        strncpy(text_path, dir[index].DIR_Name, 11);
                        
                        strncpy(input, text, 11);
                        
                        memset(temp_string, 0, 12);
                        strncpy(temp_string, "           ", 11);
                        
                        
                         char * token = strtok(input, ".");
                         strncpy(temp_string, token, strlen(token));
                         token = strtok(NULL, ".");
                        
                       
                        if ((dir[index].DIR_Attr == 0x10) || (dir[index].DIR_Attr == 0x20))
                        {
                            printf("Inside if");
                            char * token = strtok(input, ".");
                            
                            while (token != NULL)
                            {
                                strncpy(temp_string, token, strlen(token));
                                token = strtok(NULL, ".");
                                printf("%s", token);
                                strncpy(&temp_string[8], token, 3);
                            
                         
                            
                            if (token != NULL)
                            {
                                strncpy(&temp_string[8], token, 3);
                            }
                            
                                
                            }
                            int i;
                            for (i = 0; i < strlen(temp_string); i++)
                            {
                                temp_string[i] = toupper(temp_string[i]);
                            }
                            
                            if (strcmp(temp_string, text_path) == 0)
                            {
                                printf(" File Name:%s\t Attr:%d\t Low:%d\t Size:%d\n",
                                       dir[index].DIR_Name,
                                       dir[index].DIR_Attr,
                                       dir[index].DIR_FirstClusterLow,
                                       dir[index].DIR_FileSize);
                                break;
                            }
                       // }
                    }
                }
                else
                {
                    printf("Error: File system image must be opened first.\n");
                }
            }
        }   

*/
