---
title: The Loop Trap: Why Infinite AI Agents Are a Cost Problem Disguised as a Breakthrough
description: Boris Cherny's vision of continuous agentic loops is technically right. But without a budget primitive, 'continuous improvement' means 'runaway spend.'
date: 2026-06-24
---

# The Loop Trap: Why Infinite AI Agents Are a Cost Problem Disguised as a Breakthrough

The AI world is getting "loopy." At Meta's @Scale conference last week, Claude Code creator Boris Cherny made the case that agentic loops—swarms of AI agents running continuously in the background, submitting pull requests, refactoring code, never stopping—are as big a step as the shift from handwritten code to AI-written code.

He's right about the technical trajectory. He's wrong about what it costs.

## The Non-Deterministic Gamble

Cherny's demo is seductive: one agent hunts for architectural improvements, another finds duplicated abstractions. They work 24/7, submitting PRs like human teammates. The codebase evolves constantly, so they never run out of work.

Technically, this works. Recursive loops with non-deterministic termination—where a subagent decides when to stop rather than a hard condition—are a known paradigm, as Russell Brandom reports for TechCrunch. The Ralph Loop sums up a model's progress and asks if the goal is met, bouncing the agent back until completion.

The problem: "until completion" is unbounded.

## The Token Ceiling Nobody Talks About

Cherny's framework burns tokens at a rate that makes regular agentic AI look frugal. A Q&A chatbot costs pennies per query. A single agent running a task costs dollars. A continuous loop of agents improving a codebase around the clock? That's a cost function with no upper bound.

This is fine for Anthropic, whose business model is selling tokens. For everyone else—startups, mid-market engineering teams, solo developers—the loop model introduces a failure mode that doesn't exist in deterministic software: financial drift. Your agents aren't stuck in an infinite loop in the traditional sense. They're stuck in an economic loop, and you don't notice until the bill arrives.

## The Missing Guardrail

What's conspicuously absent from the loop narrative is a budget primitive. In traditional software, infinite loops crash the process. In agentic loops, they just cost money. The agent doesn't halt—it keeps "making incremental improvements" until someone manually kills it or the account runs dry.

Cherny's framework treats continuous operation as a feature. But continuous operation without a budget constraint is not autonomy. It's a runaway process with a credit card.

The industry needs a budget abstraction for loops: a declarative token ceiling, a cost-to-progress ratio that triggers a halt, or at minimum a kill switch that isn't a human watching the bill. Without it, the "loop" is less a breakthrough and more a liability wrapped in a demo.

---

*Sources:*  
*— [TechCrunch: "The AI world is getting 'loopy'"](https://techcrunch.com/2026/06/22/the-ai-world-is-getting-loopy/) by Russell Brandom*
