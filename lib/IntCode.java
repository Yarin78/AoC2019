package year2019.lib;

import java.util.*;
import java.util.concurrent.*;

public class IntCode {
    public int id;
    public int[] factorySettings;
    public int[] mem;
    public int[] instrCount;
    public Input input;
    public Output output;
    public int ip;
    public int count;  // num instructions executed
    public int lastInput, lastOutput;
    public boolean halted, blockedOnInput;

    public IntCode(int programId, String code) {
        factorySettings = Arrays.stream(code.split(",")).mapToInt(Integer::parseInt).toArray();
        reset();
        initIo(null, null);
    }

    public void reset() {
        mem = factorySettings.clone();
        ip = 0;
        count = 0;
        instrCount = new int[mem.length];
        halted = false;
        blockedOnInput = false;
    }

    public void initIo(Input input, Output output) {
        this.input = input == null ? new Pipe() : input;
        this.output = output == null ? new Pipe() : output;
    }

    public List<Integer> run(Input input, Output output) {
        return run(input, output, 0);
    }

    public List<Integer> run(Input input, Output output, int steps) {
        initIo(input, output);

        if (steps > 0) {
            while (steps > 0 && step());
        } else {
            while (step());
        }

        if (this.output instanceof Pipe) {
            return ((Pipe) this.output).getRemaining();
        }
        return null;
    }

    private static int[] numParamModeParams = new int[] {
            0,
            3, 3, 0, 1, 2, 2, 2, 2
    };

    private boolean step() {
        if (halted) {
            throw new RuntimeException("Machine already halted");
        }
        if (ip < 0 || ip >= mem.length) {
            throw new RuntimeException("Program out of bounds");
        }

        count++;
        instrCount[ip]++;

        int opcode = mem[ip] % 100;
        int paramMode = mem[ip] / 100;
        int params[] = null;
        if (opcode < numParamModeParams.length) {
            params = new int[numParamModeParams[opcode]];
            for (int i = 0; i < params.length; i++) {
                params[i] = mem[ip+i+1];  // assumes the params comes directly after the opcode
                if (paramMode % 10 == 0) {
                    params[i] = mem[params[i]];
                }
                paramMode /= 10;
            }
        }

        switch (opcode) {
            case 1: // ADD z = x + y
                mem[mem[ip+3]] = params[0] + params[1];
                ip += 4;
                break;
            case 2: // MUL z = x * y
                mem[mem[ip+3]] = params[0] * params[1];
                ip += 4;
                break;
            case 3: // IN x
                lastInput = input.get();
                mem[mem[ip+1]] = lastInput;
                ip += 2;
                break;
            case 4 : // OUT x
                lastOutput = params[0];
                output.put(params[0]);
                ip += 2;
                break;
            case 5 : // JT - IF x <> 0 JP y
                if (params[0] != 0) {
                    ip = params[1];
                } else {
                    ip += 3;
                }
                break;
            case 6 : // JF - IF x == 0 JP y
                if (params[0] == 0) {
                    ip = params[1];
                } else {
                    ip += 3;
                }
                break;
            case 7 : // LT - z = x < y ? 1 : 0
                mem[mem[ip+3]] = params[0] < params[1] ? 1 : 0;
                ip += 4;
                break;
            case 8 : // EQ - z = x == y ? 1 : 0
                mem[mem[ip+3]] = params[0] == params[1] ? 1 : 0;
                ip += 4;
                break;
            case 99: // HALT
                halted = true;
                break;
        }

        return !halted;
    }

    interface Input {
        int get();
    }

    interface Output {
        void put(int value);
    }

    public static Pipe inPipe(int[] initialData) {
        return new Pipe(initialData);
    }

    public static class Pipe implements Input, Output {
        BlockingQueue<Integer> queue = new LinkedBlockingQueue<>();

        public Integer lastGet = null, lastPut = null;

        public Pipe() {
        }

        public Pipe(int[] initialInput) {
            for (int x : initialInput) {
                queue.offer(x);
            }
        }

        public Pipe(Collection<Integer> initialInput) {
            for (int x : initialInput) {
                queue.offer(x);
            }
        }

        @Override
        public int get() {
            try {
                lastGet = queue.take();
                return lastGet;
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }

        @Override
        public void put(int value) {
            lastPut = value;
            queue.add(value);
        }

        public List<Integer> getRemaining() {
            ArrayList<Integer> result = new ArrayList<>();
            Integer el;
            while ((el = queue.poll()) != null) {
                result.add(el);
            }

            return result;
        }
    }

    public static void parallelExecute(IntCode[] programs) throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(programs.length);
        for (IntCode program : programs) {
            executor.submit(() -> {
                while (program.step());
            });
        }
        executor.shutdown();
        executor.awaitTermination(60, TimeUnit.SECONDS);
        if (!executor.isTerminated()) throw new RuntimeException("Not all programs finished");
    }
}
