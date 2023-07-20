< drac2 >
return '''name: Absorptive Armor
  automation:
    - type: counter
      counter: This does not exist at all and never should
      amount: "3"
      allowOverflow: false
      errorBehaviour: ignore
    - type: target
      target: self
      effects:
        - type: damage
          damage: -{min(3,lastCounterRequestedAmount)}[absorption]
          overheal: false
    - type: text
      text: >-
        *Crystadium, Absorptive Reinforcement, Cortosis Weave*


        When you are wearing this armor, damage that you take from weapons is reduced by 3. If this would reduce the damage to 0, the damage is instead reduced to 1. Additionally, when taking energy damage from a lightweapon, this armor's absorptive number is doubled to 6."
      title: Absorptive 3
  verb: is protected by their
  proper: true
  criton: 7
  _v: 2'''
</drac2>