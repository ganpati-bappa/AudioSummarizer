import argparse
import abs_sum
import utils
import summarize
import tensorflow as tf

API_KEY = "51490501000f4f9086206bd6af5c79d5"


def run(audio_file):
    # parser = argparse.ArgumentParser()
    # parser.add_argument('audio_file', help='url to file or local audio filename')
    # parser.add_argument('--local', action='store_true', help="Must be set, if it's a local file")
    # parser.add_argument('--api_key', action='store')
    #
    # args = parser.parse_args()
    #
    # args.api_key = API_KEY

    header = {
        'authorization': API_KEY,
        'content-type': 'application/json'
    }

    upload_url = utils.upload_file(audio_file, header)
    # if args.local:
    #
    # else:
    #     upload_url = {'upload_url': args.audio_file}

    transcript_response = utils.request_transcript(upload_url, header)

    # print(transcript_response)

    polling_endpoint = utils.make_polling_endpoint(transcript_response)

    utils.wait_for_completion(polling_endpoint, header)

    paragraphs = utils.get_paragraphs(polling_endpoint, header)
    ans_string1 = ""

    with open('transcript.txt', 'w') as f:
        for para in paragraphs:
            # print(para['text'] + '\n')
            ans_string1 += para['text']
            f.write(para['text'] + '\n')

    count = ans_string1.count(".") // 2
    summary1 = summarize.make_text(ans_string1)
    summary2 = summarize.generate_summary(ans_string1, count)
    # print(f"\nTranscript: \n{ans_string1}")
    # print(f"\n\nSentence Score Based Summary: \n{summary1}")
    # print(f"\n\nSentence Similarity based Summary: \n{summary2}")

    ret = {
        "Transcript": ans_string1,
        "Sentence Score Based Summary": summary1,
        "Similarity Based Summary": summary2
    }

    try:
        abs_summary = abs_sum.get_abstractive(ans_string1)
        ret["Abstract Summary"] = abs_summary
        # print(f"\n\nAbstractive_Summary: \n{abs_summary}")

    except:
        pass

    return ret


# if __name__ == '__main__':
#     run()
