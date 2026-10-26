# 05: Collusion-definitions survey: notes for choosing our definition

Source: `starter/collusion_hackathon/literature/definitions/README.md`, written by the organisers' starter team. It covers 139 definitions coded on 18 components; sections read: Summary, How the definitions differ, Components and clusters, and the entries for Motwani, Shlegeris, Hagag, Hu, Lee & Park 2026a, and the METR/OpenAI incident reports.

## Key takeaways

1. **There are two literatures, not one.** Economics (clusters E + F, 89 papers) judges collusion by *outcomes in a competitive market*. AI safety (cluster B, 44 papers) judges it by *unwanted, usually covert, coordination against an overseer or principal*. They share only "several parties coordinate, benefit themselves, at a third party's expense."
2. **The three most contested components are communication, intent and agreement**, exactly the elements antitrust uses to infer an agreement (plus factors). "The ML and economics literature has largely defined away the legal concept", which is directly usable for 2.3.
3. **Most AI-safety definitions describe *instructed* collusion** (they measure capability: agents told to collude) rather than **propensity**. "Emergent, not designed" is required mostly by economics definitions. That makes emergent collusion in non-market agent workflows **under-studied**.
4. **"Common cause" is the least addressed component:** only 18 definitions say whether correlated behaviour from a shared model or training run counts. For many copies of one model this is a "conspicuous gap", relevant to same-model agent teams and to same-model monitors.
5. **Monitor–policy collusion is assumed, not measured.** Nguyen (cluster C) assumes an untrusted monitor goes easy on its own model, "assumed from shared identity, not elicited or measured", and Nguyen's own trusted baseline also scored 0%, so the effect can't be attributed to collusion. Shlegeris defines collusion as the monitor lying for another instance. That makes it an open empirical question.
6. **Rose et al. draw the only formal line** between coordination (no communication, nobody harmed) and collusion (communication plus harm). Nakamura (Colosseum) adds **emergent collusion** (acted out without instruction) versus **attempted collusion / "collusion on paper"** (planned in talk, not followed in action), which is the say-vs-do split behind 2.2.
7. **Both incident reports (METR, OpenAI) fall in cluster B:** unwanted cooperation, communication present, harm to the developer's evaluation and third parties.
8. **Suggested minimal common definition** (from the survey): *two or more agents coordinate, with or without communication, in a way that benefits them at the expense of a third party, contrary to the intended competitive or oversight structure.*

## Recommendation for our report

- Adopt the **cluster-B sense** (unwanted coordination contrary to the designer's or overseer's intent), quote the survey's minimal definition, and **state explicitly** which components our operationalisation requires: multiple parties ●, coordination ●, unwanted ●, third-party harm ● (principal or non-coalition agents), communication ◐ (we measure channel use rather than assume it), intent ◐ (measured from messages or reasoning, not required).
- Use Nakamura's **emergent vs attempted** distinction as our outcome vocabulary.
- Note in Related Work that most prior work is instructed or capability-focused, and position any propensity or emergence result as new.
