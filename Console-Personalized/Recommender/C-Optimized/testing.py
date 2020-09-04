import CythonRecommender as CyRe


if __name__ == '__main__':
    factors = [1.0119084766654052, 0.2738593451543023, -0.19202096876447025, 0.16243546143742582]
    user_obj = CyRe.get_user()
    CyRe.get_recs_for_user_by_factors(user_obj, factors, progress_log=True)