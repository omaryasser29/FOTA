#__________________ Modules
from cloud import *
from STM import Serial_Port_Configuration , STM_COMMAND
import time
import os

#__________________ Main code

if __name__ == "__main__":
    
    # Check the Authentication to download 

    ret = Serial_Port_Configuration("/dev/ttyS0")
    if(ret < 0):
        print("Error in Serial Port Configuration")
        exit(1)
    else:
        print("Serial Port Configured Successfully")


    while True:
        if check_value() == 1:
            
            # Download the file
            if download_file():
                # Update the value in the database to 0
                update_value_to_zero()

                # Flash the Downloaded Code
                STM_COMMAND("FLASH")

                # Jump to User Application
                STM_COMMAND("RUN")

                # Remove the file from the cloud
                remove_file_from_cloud()

                # Remove the file from the local directory
                os.remove("./code.bin")
            else:
                print("Failed to download file.")
        else:
            print("Authentication failed. File download aborted.")
        

        time.sleep(5)


