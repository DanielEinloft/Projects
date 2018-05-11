using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;


public class UserInterface : MonoBehaviour
{

    public GameObject gameLoseUI;
    public GameObject gameWinUI;
    bool gameover;

    void Start()
    {
        Guard.OnGuardHasSpottedPlayer += ShowGameLoseUI;
        //FindObjectOfType<Player>().WinLevel += ShowGameWinUI;
    }


    void Update ()
    {
    	if(gameover)
        {
            if(Input.GetKeyDown(KeyCode.Space))
            {
                SceneManager.LoadScene(0);

            }
        }
	}

    void ShowGameWinUI()
    {
        OnGameOver(gameWinUI);
    }

    void ShowGameLoseUI()
    {
        OnGameOver(gameLoseUI);

    }

    void OnGameOver(GameObject gameOverUI)
    {
        gameOverUI.SetActive(true);
        gameover = true;
        Guard.OnGuardHasSpottedPlayer -= ShowGameLoseUI;
        //FindObjectOfType<Player>().WinLevel -= ShowGameWinUI;

    }

}
