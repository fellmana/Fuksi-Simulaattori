"""Mode containing commandline argument parsing options"""
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--map",type = str.lower, choices=["kumpula","areena"],default="kumpula",
                        help="Define the map of the simulation")
    parser.add_argument("-f","--fuksi",type=int, default=200,
                        help="Number of fuksi")
    parser.add_argument("-o","--opiskelija",type=int,default=50,
                        help="number of opiskelija")
    parser.add_argument("-p","--proffa",type=int, default=30,
                        help="number of proffa")
    parser.add_argument("-l","--language",type = str.lower, choices=["fin","eng","swe"],default="fin",
                        help="Define language options")
    parser.add_argument("--debug",action="store_true",default=False,
                        help="Enable debugging options")
    args = parser.parse_args()
    

    return args