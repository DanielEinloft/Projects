using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Score : MonoBehaviour
{

    public Text score;
    public int ballValue;

    public int scoreValue = 0;

	
    void OnTriggerEnter2DD()
    {
        scoreValue += ballValue;
        UpdateScore();
    }
    void UpdateScore()
    {
        score.text = "Score: " + scoreValue;
    }
}
