libRadtran
==========
>a package for radiative transfer calculations in the ultraviolet, visible, and infrared

>version 1.7

>last_update_time: 2014-10-24

>reference:

>1. http://www.libradtran.org/doku.php
>2. Mayer B, Kylling A, Emde C, et al. libRadtran user’s guide[J]. 2011.
>3. Mayer B, Kylling A. Technical note: The libRadtran software package for radiative transfer calculations-description and examples of use[J]. Atmospheric Chemistry and Physics, 2005, 5(7): 1855-1877.

###Get the distribution [link](http://www.libradtran.org/doku.php?id=download)

###Unpack the distribution

    gzip -d libradtran-1.7.tar.gz
    
###Required software to build libRadtran
>1. GUN make, gcc, python
>2. gfortran (sudo apt-get install gfortran)
>3. gsl 1.16 (GUN Scientific Library)
>>      ./configure, make, make check, make install
>4. m4 1.4.17
>>      ./configure, make, make check, make install
>5. gmp 5.1.3
>>      ./configure, make, make check, make install
>6. zlib 1.2.8
>>      ./configure, make, make check, make install
>7. netcdf 4.2
>>      ./configure --disable-dap  --disable-netcdf-4  --disable-doxygen, make, make check, make install
>8. 环境变量
>>      sudo gedit ~/.bashrc

>>>最后加入:

>>>     export PATH=/usr/local/netcdf/bin:$PATH

>>>     export LD_LIBRARY_PATH=/usr/local/netcdf/lib:$LD_LIBRARY_PATH

>>>     export DYLD_LIBRARY_PATH=/usr/local/netcdf/lib:$DYLD_LIBRARY_PATH

>>>     source ~/.bashrc 使上述设置生效, 终端执行 nc-config 按照提示操作
###Compile the distribution

    cd libRadtran-1.7
    ./configure (看能否找到上述包的安装目录, 如无误, 则继续)
    make
    make check
###Python package
(推荐使用Anaconda，可以简化不同包之间的依赖关系)

    sudo apt-get install python-scipy
    sudo apt-get install python-numpy
    sudo apt-get isstall python-matplotlib
### Water clouds, ice clouds, OPAC aerosols [link](http://www.meteo.physik.uni-muenchen.de/~libradtran/lib/exe/fetch.php?media=download:optprop_v2.0.tar.gz)
> Please untar these data in the libRadtran directory:

> ~/libRadtran-1.7/data/aerosol/OPAC

> ~/libRadtran-1.7/data/wc/mie

> ~/libradtran-1.7/data/ic

###Examples to use libRadtran
> Put files mystic.inp, mystic_run.inp, polarization.py in directory ~/libRadtran-1.7/bin

> run polarization.py


