export const TEST_SCENARIO_DEPRESSION = {
    patientId: "TEST-PT-101",
    sessionDate: new Date().toISOString().split('T')[0],
    transcript: `
DOCTOR: Good morning, Sarah. How have you been feeling since our last session?

PATIENT: Honestly, Dr. Smith, it's been a rough couple of weeks. I'm just feeling so drained all the time. I can barely get out of bed in the mornings.

DOCTOR: I'm sorry to hear that. When you say drained, do you mean physically tired, or is it more of a lack of motivation?

PATIENT: It's both. I wake up and I just want to pull the covers back over my head. I've missed three days of work this week. I just don't see the point in going.

DOCTOR: Missing work is a significant change for you. Have you been noticing any changes in your appetite or sleep patterns?

PATIENT: Yeah, I'm not really hungry. I've lost maybe 5 pounds. And sleep... I fall asleep okay, but I wake up at like 3 AM and can't go back to sleep. My mind just starts racing.

DOCTOR: What kinds of thoughts are racing through your mind at 3 AM?

PATIENT: Just... that I'm failure. That I'm letting everyone down. My husband, my kids. Sometimes I think they'd be better off without me dragging them down.

DOCTOR: Sarah, that's a very heavy thought to carry. When you say they'd be better off, have you had any thoughts of hurting yourself?

PATIENT: No, no, I wouldn't do that. I couldn't do that to them. But I just wish I could disappear sometimes.

DOCTOR: Thank you for sharing that with me. It sounds like you're experiencing some significant depressive symptoms—the fatigue, the early morning awakening, the guilt, and the passive thoughts of death. How have you been doing with the Sertraline we started last month?

PATIENT: I'm taking it every day, the 50mg. But I don't feel like it's doing anything yet. 

DOCTOR: It can take a bit of time, but at 4 weeks we usually hope to see some spark. Given the severity of what you're describing, I'm wondering if we should increase the dose to 100mg.

PATIENT: I'm willing to try anything at this point.

DOCTOR: Okay. We'll increase the Sertraline to 100mg daily. I also want to check something—have you ever had periods where you felt the opposite? Like you didn't need sleep, had tons of energy, or did things that were out of character for you?

PATIENT: No, never. I've always been more on the low side if anything.

DOCTOR: Okay, that's helpful to rule out other things. So, plan for today: Increase Sertraline to 100mg. I also want you to try to take a 10-minute walk outside each morning, just to get some light. Can we try that?
`.trim(),
    soapNotes: ""
};
