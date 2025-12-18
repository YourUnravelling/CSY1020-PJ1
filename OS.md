

## OS
A collection of system programs 
Helps a programmer interface with the computer beyond the simple system commands

### Kernel
Central part of the OS
All hardware requests go through it as system calls

### Shell
Interface between apps and the kernel

### Interrupts
Where the normal running of a program is interrupted by an event.
- By hardware eg key presses
- Within the cpu by an unexpected event like a divide by 0 error
- External events like interface cards
- 



### File system & users
Organises and accesses files, controls access to files


### API
Interface between the app and the OS
Provides system services to applications.

### User interface

Consistant interface between the user and OS

## Single user/task system
Single machine running one app at a time
ATM machines, printers

## Multi tasking OS


### multiprocessing 
Where many programs are run for a short amount of time, to create the appearence of them running at once.





1. To manage application's interfaces with hardware


# Processes

A process consists of:
- The executable program
Includes processor context but also things like the process id, priority level, and state.
- The data ascociated with the program
- Execution context


## Process states

Ready dispatch-> <-Timeout Running
 /\              \/
 Event           Wait on event
        Blocked         

The process switches between the ready and running states, only running for a small time before a timeout switches it back to ready and another process can run.
If a process is blocked while running, the OS is free to schedule another process

## Process scheduling

### Round-robin
A simple approach, each process is forced to give up control when its time is up.
Sometimes called pre-emptive scheduling

## Interprocess communication
Processes need to communicate with others, for example when both operating on the same resources

### Mutual exclusion
Mutual exclusion is where a program has full control of a resource (file, printer, ect)
A resource is pre-emptive if ownership of it can be taken away from one process and given to another

Mutual exclusion makes sure no two programs are in critical parts of their code, and letting them finish to not corrupt resources.

### Synchronisation
Synchronised processes must be managed, for example two programs which both use the same buffer, one writng and one reading
One approach is using flags which indicate when resources are available.
A program can see the process does not have a flag and sets it for the duration of its use of the resource, other processes can check the flag to see if the resource is available, or if they are 'locked out'

fttf ****
tttt ****
fttf ****
tttt ****
ff   *x

1. Ready, running, blocked, not running, running, waiting for an event so it can continue running.
2. process id, priority, state


# I/O
the i/o system layer controls how peripherals ad system components talk to each other
EG when deleting a file the i/o operates on the disk and the filesystem

## Drivers
Every I/O device has a driver to allow the OS's general commands to be converted into the spesific signals for the device, and vice versa
Sometimes an OS can have common drivers installed
Device drivers perform the same functions as basic I/O, but just for one device
The I/O system can sometimes be thought of as a set of basic preinstalled drivers.

## Resource sharing
What the resource is determines how it can be shared, for example only one process can use a printer.

## Daemons
UNIX uses program daemons, to organise requests for data transfer between a device and multiple users
Process requests are placed into a queue

## Spooling (Simeltaneous peripheral output online)
Stores peropheral requests in a queue until dealt with
Tend to be for output only

## DMA
Allows data to be transferred between memory and the device as fast as possible
- Network cards
- Scanners
- Hard disks

the I/O's role in DMA is to organise details such as the memory locations, read/write, and which line/channel is to be used.


tfft ****
Tftt ****
fttf ****
tft  ***