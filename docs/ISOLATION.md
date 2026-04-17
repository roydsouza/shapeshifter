# Strategic Research: Cage Host-Effect Containment (Task 012)

## 1. Problem Statement: The "Side-Effect Leak"
Current Shapeshifter implementation uses **Step-Based Gas Limits** to prevent infinite loops (CPU exhaustion). However, there is a "Gap 5" in our security architecture: **Host-Side Effects**.

When the agent evaluates a mutation in a `run_with_gas` block, that mutation is still running in the host Python environment. Any state change, I/O operation, or network call it triggers is **irreversible**, even if the mutation's gas limit is eventually hit or the mutation is discarded as "low fitness."

### The Risk of Autonomous Evolution
As we move to Phase 2 (Darwinian loop), the agent will be proposing *hundreds* of code variants. If one of those variants contains a bug—or an emergent "adversarial" trait—that attempts to delete a file or corrupt a database, the current cage will not stop it.

---

## 2. Alternatives Considered

We have evaluated four primary candidates for sealing Gap 5, ranging from language-level restrictions to OS-level isolation.

### A. Monadic Effect-Tracking
- **Description**: Tagging every function in the environment as either `Pure` or `Impure`. The interpreter refuses to run `Impure` functions within a mutation sandbox.
- **Trade-offs**: 
    - *Pros*: Extremely fast; zero overhead.
    - *Cons*: Prevents the agent from experimenting with its own I/O logic. It makes the sandboxed world "lossy" and less useful for real-world agent tasks.

### B. Capability-Based Environments (Environment Switching)
- **Description**: When `run_with_gas` is called, the interpreter swaps the `global_env` for a restricted **Sub-Environment**. 
- **Mechanism**: Symbols like `print` are replaced by "Capability Mocks" that provide a safe, restricted interface.
- **Trade-offs**:
    - *Pros*: Flexible; allows us to provide "virtualized" versions of real functions.
    - *Cons*: We must be careful not to miss any "leaky" symbols in the default env.

### C. Buffered Reality (The "Staging Area" Model)
- **Description**: Side effects are not executed immediately; they are written to a **Side-Effect Buffer**.
- **Mechanism**: If a code variant wins the Darwinian selection, its buffer is "flushed" to the real host environment. If it is discarded, the buffer is purged.
- **Trade-offs**:
    - *Pros*: Provides a true "undo" for reality; allows mutations to behave as if they are in the real world without the risk.
    - *Cons*: Complexity in implementing "Undo" for irreversible actions like physical I/O or network packets.

### D. Process-Level Isolation (Subprocess)
- **Description**: Each mutation evaluation runs in a separate, low-privilege OS process (e.g., using `sandbox-exec` on macOS or `seccomp` on Linux).
- **Trade-offs**:
    - *Pros*: Absolute containment; even a 0-day in Python would be trapped.
    - *Cons*: High context-switching overhead (~10-100ms per variant), making "brood" evaluation (100+ candidates) very slow.

---

## 3. The Selected Strategy: Hybrid Capability-Buffering

We have selected a **Hybrid Staging Model** for Phase 2. This represents the best balance between high-frequency experimentation and safety.

### Phase 2a Implementation Objectives:
1. **Isolated Environments**: `evaluate` will be updated to support an `explicit_env`. Mutations will be run in environments containing *only* whitelisted symbols.
2. **Virtual I/O Buffering**: 
    - Replace the host `print` with a `virtual_buffer` version. 
    - The Darwinian loop will inspect the buffer to verify the mutation's output *before* deciding to commit.
3. **Transactionality**: All "side effects" proposed by a mutation must be treated as a transaction.
    - `proposal` → `buffered evaluation` → `selection` → `commit (flush)` OR `discard (purge)`.

### 3.1 The Phase 2a Whitelist (Ground Truth)

The following symbols represent the **Maximum Permitted Capability** for any sandboxed code in Phase 2a. Any symbol not on this list will be REJECTED with a `CapabilityError`.

| Category | Symbols |
|---|---|
| **Arithmetic** | `add`, `sub`, `mul`, `div` |
| **Logic** | `gt`, `lt`, `eq` |
| **Data (Lists)** | `list`, `first`, `rest`, `cons` |
| **Control** | `if`, `quote`, `set`, `defn`, `lambda`, `begin` |

**Note**: Special forms (`if`, `quote`, `set`, `defn`, `lambda`, `begin`) are structurally handled by the `evaluate` loop, but `defn`, `lambda`, and `begin` are now explicitly permitted in the sandbox to allow sequenced local function definitions.

**Dynamic Capabilities (Injected by Caller):**
- `print`: Must be a buffered mirror, never the host `print`.
- `get_metrics`: Explicitly restricted for Phase 2a (see Task 015).

---

## 4. Philosophical Implications: "The Staged Reality"

This choice aligns with our **Human-in-the-Loop (HITL)** mandate. By buffering effects, we give Roy (and the Crucible) a chance to inspect the "intent" of the code before it impacts the station or the world.

> "A mutation is a hypothesis about reality. It should not be allowed to change reality until the hypothesis is proven." — *Shapeshifter Design Invariant*

---

## 5. Analyst Review Triggers
This strategy implies moving from **Unrestricted Symbolic Execution** to **Capability-Gated Execution**. 
- **Escalation**: Implementation of the Environment White-listing must be reviewed by the Analyst, as it is the "Frontier" of the security cage.
- **Verification**: Proof of Concept will demonstrate a mutation attempting to access a forbidden symbol (e.g., `os.system`) and failing.
