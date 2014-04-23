/*** _kernelFileIO(file_path,value_that_has_to_be_written_to_the_file)
This function takes the file path and opens the file in read-write mode.
If arg2 is 'none';it returns the contents of the file
If arg2 is a value; it write the value into the file and returns the value
Returns NULL when python arguments aren't succesfully converted to C
***/

#include "Python.h"

static PyObject* _kernelFileIO(PyObject *self, PyObject *args)
{ 
  FILE* fd;
  int rd;
  char *val;
  char *fn; 
	
  //Converts the file path into a string
  if(!(PyArg_ParseTuple(args,"s",&fn)))
		return NULL;

  //Converts the value to a C string	
  if(!(PyArg_ParseTuple(&args[1],"s",&val)))
		return NULL;
	
  fd = fopen(fn,"r+");
  if(fd==NULL)
    return NULL;
  fseek(fd,0,SEEK_SET);

  if (val!=NULL)
  {
    fprintf(fd,"%s",val);
  }
  fscanf(fd,"%d",&rd);
  return Py_BuildValue("i",rd);
}       

static PyMethodDef sysfsMethods[]=
{
	{ "_kernelFileIO", _kernelFileIO, METH_VARARGS },
	{ NULL, NULL },
};

PyMODINIT_FUNC init_sysfs(void)
{
	Py_InitModule("_sysfs",sysfsMethods);
}

