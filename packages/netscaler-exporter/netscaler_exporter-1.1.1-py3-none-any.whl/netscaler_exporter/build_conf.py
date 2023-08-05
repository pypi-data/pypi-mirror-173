import sys, os, argparse, inspect, shutil
from netscaler_exporter.netscaler_exporter import get_module_path

#******************************************************************************************
class myArgs:
  attrs = [ 'config_path', 'dry_mode', 'overwrite'
          ]
  def __init__(self):

    for attr in myArgs.attrs:
        setattr(self, attr, None)


#******************************************************************************************
def main():

   # get command line arguments

   parser = argparse.ArgumentParser(description='build config directory for netscaler_exporter.')
   parser.add_argument('-c', '--config_path'
                        , help='set config directory to copy default files.')

   parser.add_argument('-n ', '--dry_mode'
                        , action='store_true'
                        , help='do not perform any action; just check what will be performed.'
                        , default=False
                )

   parser.add_argument('-o ', '--overwrite'
                        , action='store_true'
                        , help='if config_path already exists overwrite or not.'
                        , default=False
                )

   inArgs = myArgs()
   args = parser.parse_args(namespace=inArgs)

   config_path = './conf'
   if args.config_path is not None:
      config_path = inArgs.config_path

   if args.dry_mode:
      dry_mode_str = '[check_mode] '
   else:
      dry_mode_str = ''

   if not os.path.exists(config_path):
      pass
      # do nothing since shutil.copytree() will create the directory and raise exception if it exists!
#      if not args.dry_mode:
#         os.mkdir( config_path )
#      print( '{0}{1} directory created'.format(dry_mode_str, config_path) )
   elif not os.path.isdir(config_path):
      print( '{0}error: {1} is not a directory'.format(dry_mode_str, config_path) )
      sys.exit(1)
   else:
      print( '{0}warning: {1} directory already exists'.format(dry_mode_str, config_path) )
      if not args.overwrite:
         print('{0}ok: no copy performed. (overwrite is False)'.format(dry_mode_str))
         sys.exit(0)

   netscaler_path = get_module_path()
   if netscaler_path is not None:
      print('{0}path for module netscaler_exporter is : {1}'.format( dry_mode_str, netscaler_path ))
   else:
      print('{0}error: path for module netscaler_exporter not found!'.format(dry_mode_str))
      sys.exit(1)

   if not args.dry_mode:
      shutil.copytree(netscaler_path + '/conf/', config_path)
   print('{0}ok: files copied in {1}'.format(dry_mode_str, config_path))
   sys.exit(0)

# end main...

#*****************************************************************************
if __name__  == '__main__':
   main()

