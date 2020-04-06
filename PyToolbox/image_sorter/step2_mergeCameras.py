#! python3
## STEP 1: Sort images and rename them based on QR codes
import  merger
import sys

def main(rootpath=sys.argv[0]):
    merger(rootpath)
    print('All done')
    print('[IMPORTANT]: Please double check the work is done properly. If so, remove RC and LC folders.')
    print('[IMPORTANT]: After removing RC and LC there is not way back!!!')
    
    
if __name__ == "__main__":
    main()
    