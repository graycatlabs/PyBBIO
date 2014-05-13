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
  char rd[64];
  char *val;
  char *fn; 
	
  //Converts the file path into a string
  if(!(PyArg_ParseTuple(args,"ss",&fn, &val)))
		return Py_BuildValue("");
	
  fd = fopen(fn,"r+");
  if(fd==NULL)
    		return Py_BuildValue("");
  fseek(fd,0,SEEK_SET);

  if (val!=NULL)
  {
    fprintf(fd,"%s",val);
  }
  fgets(rd,64,fd);
  return Py_BuildValue("s",rd);
}       

static PyMethodDef sysfsMethods[]=
{
	{ "_kernelFileIO", _kernelFileIO, METH_VARARGS, "function that opens and r/w to a file" },
	{ NULL, NULL },
};

PyMODINIT_FUNC init_sysfs(void)
{
	Py_InitModule( "_sysfs" , sysfsMethods , "Initiate Module" );
}

