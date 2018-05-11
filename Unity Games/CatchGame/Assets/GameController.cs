using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class GameController : MonoBehaviour
{
    float leftTop = -9f;
    float rightTop = 9f;

    public float timeLeft = 10f;
    public GameObject ball;
    public Text timerText;


    private void Start()
    {
        float ballWidth = ball.GetComponent<Renderer>().bounds.extents.x;
        StartCoroutine(Spawn());
    }

    private void FixedUpdate()
    {
        if (timeLeft < 0)
            timeLeft = 0;
        else
            timeLeft -= Time.deltaTime;

        timerText.text = "Time Left: " + ((int)timeLeft).ToString();
    }

    IEnumerator Spawn()
    {
        while(timeLeft >0)
        {
            Vector3 spawnPosition = new Vector3(Random.Range(leftTop, rightTop), transform.position.y, 0f);
            Quaternion spawnRotation = Quaternion.identity;
            Instantiate(ball, spawnPosition, spawnRotation);

            yield return new WaitForSeconds(Random.Range(1f, 2f));
        }

    }


}
