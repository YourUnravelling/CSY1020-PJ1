


### CISC
The first computers 

### RISC

### RISC has not replaced CISC completely
Intel processrs use a RISC core for simple instructions and a CISC style logical system for backwards compatibility

## General constraints for hardware design

- All instructions are directly executed by hardware
No interpreter, leading to higher speeds
In CISCs, the instructions are split into multiple simpler instructions. If these are not frequently used then it is acceptable.

- Maximise rate at which instructions are issued
By using parralelism

- Instructions should be easy to decode
They should be short and fixed length, and have a small number of feilds

- Only load and stores shuld reference memory
Data and instructions should be brought to the CPU before processing

- Plenty of registers
Accessing memory is slow, so once data is fetched it should be kept. Up to 32 registers should be used.








1. Reduced instruction set...lmf n
2. Backwards compatibility
3. use lots of registers, don't access memory without going through the load and stores
