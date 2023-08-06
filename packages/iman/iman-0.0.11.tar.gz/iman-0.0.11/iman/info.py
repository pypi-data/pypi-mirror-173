import torch
import multiprocessing


def get():
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  if (str(device) == "cuda"):
     a = torch.cuda.get_device_properties(device)
     memory = a.total_memory*1e-9
     GPU_Name = a.name
     multi_processor_count=a.multi_processor_count  
  else:
    memory=0
    GPU_Name ='No GPU'
    multi_processor_count=0
    
  cpu_count  = multiprocessing.cpu_count()
  
  print('Device== ' + str(device))
  print('GPU Memory== ' + str(memory) + ' GB')
  print('GPU_Name== ' + str(GPU_Name))
  print('multi_processor_count== ' + str(multi_processor_count))
  print('CPU Count== ' + str(cpu_count))
  
  return({'device':str(device) , 'memory':memory , 'cpu_count':cpu_count , 'multi_processor_count':multi_processor_count , 'name':GPU_Name })  
      

